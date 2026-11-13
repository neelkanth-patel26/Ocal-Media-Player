"""Media artwork extraction, caching, and fallback generation for GNS Player."""
import base64
import ctypes
from ctypes import wintypes, Structure, c_void_p, byref, POINTER, WINFUNCTYPE, c_int
from pathlib import Path

from PySide6.QtGui import QPixmap, QPainter, QPainterPath, QColor, QPen, QLinearGradient, QImage
from PySide6.QtCore import Qt, QRectF, QRect

from .win11 import WIN11_ACCENT, is_windows_light_theme, get_windows_accent_palette
from .icons import get_icon

_ART_CACHE = {}
_ACTIVE_ACCENT = None
_ACTIVE_IS_LIGHT = None


def set_active_accent(accent, is_light=None):
    """Set global active application accent color and theme mode for fallbacks."""
    global _ACTIVE_ACCENT, _ACTIVE_IS_LIGHT
    _ACTIVE_ACCENT = accent
    if is_light is not None:
        _ACTIVE_IS_LIGHT = is_light


class _GUID(Structure):
    _fields_ = [
        ('Data1', wintypes.DWORD),
        ('Data2', wintypes.WORD),
        ('Data3', wintypes.WORD),
        ('Data4', wintypes.BYTE * 8)
    ]


class _SIZE(Structure):
    _fields_ = [('cx', wintypes.LONG), ('cy', wintypes.LONG)]


class _BITMAPINFOHEADER(Structure):
    _fields_ = [
        ('biSize', wintypes.DWORD), ('biWidth', wintypes.LONG),
        ('biHeight', wintypes.LONG), ('biPlanes', wintypes.WORD),
        ('biBitCount', wintypes.WORD), ('biCompression', wintypes.DWORD),
        ('biSizeImage', wintypes.DWORD), ('biXPelsPerMeter', wintypes.LONG),
        ('biYPelsPerMeter', wintypes.LONG), ('biClrUsed', wintypes.DWORD),
        ('biClrImportant', wintypes.DWORD),
    ]


def image_from_shell_bitmap(hbitmap):
    """Read either bitmap orientation as explicit top-down, opaque BGRA pixels."""
    gdi = ctypes.WinDLL('gdi32')
    gdi.CreateCompatibleDC.argtypes = [wintypes.HDC]
    gdi.CreateCompatibleDC.restype = wintypes.HDC
    gdi.DeleteDC.argtypes = [wintypes.HDC]
    gdi.DeleteDC.restype = wintypes.BOOL
    gdi.GetDIBits.argtypes = [wintypes.HDC, wintypes.HBITMAP, wintypes.UINT,
                             wintypes.UINT, c_void_p, c_void_p, wintypes.UINT]
    gdi.GetDIBits.restype = c_int
    dc = gdi.CreateCompatibleDC(None)
    if not dc:
        return QImage()
    try:
        header = _BITMAPINFOHEADER()
        header.biSize = ctypes.sizeof(header)
        if not gdi.GetDIBits(dc, hbitmap, 0, 0, None, byref(header), 0):
            return QImage()
        width, height = header.biWidth, abs(header.biHeight)
        if width <= 0 or height <= 0 or width * height > 16_777_216:
            return QImage()
        # Negative height asks GDI to normalize the row order, including bottom-up
        # video thumbnail DIBs that Qt's direct HBITMAP conversion can invert.
        header.biHeight = -height
        header.biPlanes = 1
        header.biBitCount = 32
        header.biCompression = 0  # BI_RGB
        header.biSizeImage = width * height * 4
        header.biClrUsed = header.biClrImportant = 0
        pixels = ctypes.create_string_buffer(header.biSizeImage)
        if gdi.GetDIBits(dc, hbitmap, 0, height, pixels, byref(header), 0) != height:
            return QImage()
        return QImage(pixels.raw, width, height, width * 4, QImage.Format.Format_RGB32).copy()
    finally:
        gdi.DeleteDC(dc)


_IID_IShellItemImageFactory = None


def _get_shell_image_factory_iid():
    global _IID_IShellItemImageFactory
    if _IID_IShellItemImageFactory is None:
        try:
            ole32 = ctypes.oledll.ole32
            ole32.CoInitialize(None)
            iid = _GUID()
            # Windows Shell IShellItemImageFactory GUID: {bcc18b79-ba16-442f-80c4-8a59c30c463b}
            hr = ole32.IIDFromString('{bcc18b79-ba16-442f-80c4-8a59c30c463b}', byref(iid))
            if hr == 0:
                _IID_IShellItemImageFactory = iid
        except Exception:
            pass
    return _IID_IShellItemImageFactory


def extract_windows_thumbnail(file_path, size=140):
    """
    Extract real video or image thumbnail frame using native Windows Shell IShellItemImageFactory.
    Uses SIIGBF_THUMBNAILONLY (0x08) to guarantee Windows NEVER returns an application icon.
    """
    try:
        p = Path(file_path)
        if not p.is_file():
            return None

        iid = _get_shell_image_factory_iid()
        if not iid:
            return None

        shell32 = ctypes.windll.shell32
        p_factory = c_void_p()
        hr = shell32.SHCreateItemFromParsingName(
            str(p.resolve()),
            None,
            byref(iid),
            byref(p_factory)
        )
        if hr != 0 or not p_factory.value:
            return None

        vtable = ctypes.cast(p_factory, POINTER(POINTER(c_void_p))).contents
        # vtable[3]: IShellItemImageFactory::GetImage(SIZE size, SIIGBF flags, HBITMAP* phbm)
        # Use c_int return type so ctypes does not raise unhandled OSError on non-zero HRESULT
        GetImage = WINFUNCTYPE(c_int, c_void_p, _SIZE, c_int, POINTER(wintypes.HBITMAP))(vtable[3])
        # vtable[2]: IUnknown::Release
        Release = WINFUNCTYPE(wintypes.ULONG, c_void_p)(vtable[2])

        hbitmap = wintypes.HBITMAP()
        req_size = _SIZE(size, size)
        # SIIGBF_THUMBNAILONLY (0x08) = return only thumbnail, NEVER icon
        # SIIGBF_BIGGERSIZEOK (0x01) = allows scaling from larger thumbnail
        flags = 0x08 | 0x01
        try:
            hr_img = GetImage(p_factory, req_size, flags, byref(hbitmap))
        except Exception:
            hr_img = -1
        Release(p_factory)

        if hr_img == 0 and hbitmap.value:
            try:
                qimg = image_from_shell_bitmap(hbitmap)
            finally:
                delete_object = ctypes.windll.gdi32.DeleteObject
                delete_object.argtypes = [wintypes.HGDIOBJ]
                delete_object.restype = wintypes.BOOL
                delete_object(hbitmap)
            if not qimg.isNull():
                return QPixmap.fromImage(qimg)
    except Exception:
        pass
    return None


def parse_id3_apic_data(data, version=3):
    """Parse ID3v2 APIC/PIC frames from raw ID3 tag bytes, preferring front covers."""
    pos = 0
    covers = []
    magic_headers = (b'\xff\xd8\xff', b'\x89PNG', b'GIF8', b'RIFF')

    while pos + 10 < len(data):
        if version in (3, 4):
            frame_id = data[pos : pos + 4]
            if frame_id == b'\x00\x00\x00\x00':
                break
            if version == 4:
                frame_size = (
                    ((data[pos + 4] & 0x7F) << 21)
                    | ((data[pos + 5] & 0x7F) << 14)
                    | ((data[pos + 6] & 0x7F) << 7)
                    | (data[pos + 7] & 0x7F)
                )
            else:
                frame_size = int.from_bytes(data[pos + 4 : pos + 8], 'big')
            pos += 10
            if frame_id == b'APIC' and frame_size > 8 and pos + frame_size <= len(data):
                frame = data[pos : pos + frame_size]
                enc = frame[0]
                mime_end = frame.find(b'\x00', 1)
                if mime_end != -1 and mime_end + 1 < len(frame):
                    pic_type = frame[mime_end + 1]
                    img_data = None
                    # Find exact image magic header
                    for magic in magic_headers:
                        m_pos = frame.find(magic, mime_end + 2)
                        if m_pos != -1:
                            img_data = frame[m_pos:]
                            break
                    if not img_data:
                        desc_start = mime_end + 2
                        desc_end = frame.find(b'\x00\x00' if enc in (1, 2) else b'\x00', desc_start)
                        if desc_end != -1:
                            img_start = desc_end + (2 if enc in (1, 2) else 1)
                            img_data = frame[img_start:]
                    if img_data and len(img_data) > 32:
                        covers.append((pic_type, img_data))
            pos += frame_size
        elif version == 2:
            frame_id = data[pos : pos + 3]
            if frame_id == b'\x00\x00\x00':
                break
            frame_size = int.from_bytes(data[pos + 3 : pos + 6], 'big')
            pos += 6
            if frame_id == b'PIC' and frame_size > 6 and pos + frame_size <= len(data):
                frame = data[pos : pos + frame_size]
                desc_end = frame.find(b'\x00', 5)
                if desc_end != -1:
                    img_data = frame[desc_end + 1 :]
                    if len(img_data) > 32:
                        covers.append((3, img_data))
            pos += frame_size
        else:
            break

    if covers:
        # Prioritize front cover (3), then other images, avoiding file icon (1, 2)
        covers.sort(key=lambda c: 0 if c[0] == 3 else (2 if c[0] in (1, 2) else 1))
        return covers[0][1]
    return None


def extract_id3_artwork(file_path):
    """Extract embedded ID3v2 APIC or PIC album artwork bytes from MP3."""
    try:
        with open(file_path, 'rb') as f:
            header = f.read(10)
            if header[:3] != b'ID3':
                return None
            version = header[3]
            tag_size = (
                ((header[6] & 0x7F) << 21)
                | ((header[7] & 0x7F) << 14)
                | ((header[8] & 0x7F) << 7)
                | (header[9] & 0x7F)
            )
            data = f.read(min(tag_size, 1024 * 1024 * 16))
            return parse_id3_apic_data(data, version)
    except Exception:
        pass
    return None


def extract_flac_artwork(file_path):
    """Extract embedded PICTURE block bytes from FLAC."""
    try:
        with open(file_path, 'rb') as f:
            if f.read(4) != b'fLaC':
                return None
            covers = []
            while True:
                header = f.read(4)
                if len(header) < 4:
                    break
                is_last = header[0] & 0x80
                block_type = header[0] & 0x7F
                block_len = int.from_bytes(header[1:4], 'big')
                if block_type == 6:  # PICTURE
                    block = f.read(block_len)
                    if len(block) >= 32:
                        pic_type = int.from_bytes(block[0:4], 'big')
                        mime_len = int.from_bytes(block[4:8], 'big')
                        pos = 8 + mime_len
                        if pos + 4 <= len(block):
                            desc_len = int.from_bytes(block[pos : pos + 4], 'big')
                            pos += 4 + desc_len + 16
                            if pos + 4 <= len(block):
                                data_len = int.from_bytes(block[pos : pos + 4], 'big')
                                pos += 4
                                img_data = block[pos : pos + data_len]
                                if len(img_data) > 32:
                                    covers.append((pic_type, img_data))
                else:
                    f.seek(block_len, 1)
                if is_last:
                    break
            if covers:
                covers.sort(key=lambda c: 0 if c[0] == 3 else (2 if c[0] in (1, 2) else 1))
                return covers[0][1]
    except Exception:
        pass
    return None


def extract_mp4_artwork(file_path):
    """Extract embedded covr atom image bytes from M4A / MP4 / AAC."""
    try:
        p = Path(file_path)
        size = p.stat().st_size
        with open(file_path, 'rb') as f:
            data = f.read(min(size, 1024 * 1024 * 8))
            covr_idx = data.find(b'covr')
            if covr_idx == -1 and size > 1024 * 1024 * 8:
                # Many M4A files keep the moov atom at the end of the file
                f.seek(max(0, size - 1024 * 1024 * 8))
                data = f.read(1024 * 1024 * 8)
                covr_idx = data.find(b'covr')

            if covr_idx != -1:
                data_idx = data.find(b'data', covr_idx)
                if data_idx != -1 and data_idx - covr_idx < 64:
                    atom_size = int.from_bytes(data[data_idx - 4 : data_idx], 'big')
                    img_data = data[data_idx + 12 : data_idx - 4 + atom_size]
                    if len(img_data) > 32:
                        return img_data
    except Exception:
        pass
    return None


def extract_ogg_artwork(file_path):
    """Extract embedded METADATA_BLOCK_PICTURE from Ogg Vorbis or Opus."""
    try:
        with open(file_path, 'rb') as f:
            data = f.read(1024 * 1024 * 4)
            for tag in (b'METADATA_BLOCK_PICTURE=', b'metadata_block_picture='):
                idx = data.find(tag)
                if idx != -1:
                    val_start = idx + len(tag)
                    val_end = val_start
                    while val_end < len(data) and (
                        data[val_end:val_end+1].isalnum()
                        or data[val_end:val_end+1] in b'+/=\r\n'
                    ):
                        val_end += 1
                    b64_bytes = data[val_start:val_end].strip()
                    if b64_bytes:
                        raw_flac_pic = base64.b64decode(b64_bytes)
                        if len(raw_flac_pic) > 32:
                            mime_len = int.from_bytes(raw_flac_pic[4:8], 'big')
                            pos = 8 + mime_len
                            desc_len = int.from_bytes(raw_flac_pic[pos : pos + 4], 'big')
                            pos += 4 + desc_len + 16
                            data_len = int.from_bytes(raw_flac_pic[pos : pos + 4], 'big')
                            pos += 4
                            return raw_flac_pic[pos : pos + data_len]
    except Exception:
        pass
    return None


def extract_wav_artwork(file_path):
    """Extract embedded ID3 chunk artwork from WAV file."""
    try:
        with open(file_path, 'rb') as f:
            riff = f.read(12)
            if riff[:4] != b'RIFF' or riff[8:12] != b'WAVE':
                return None
            while True:
                chunk_header = f.read(8)
                if len(chunk_header) < 8:
                    break
                cid = chunk_header[:4]
                clen = int.from_bytes(chunk_header[4:8], 'little')
                if cid.lower() == b'id3 ':
                    id3_data = f.read(clen)
                    if id3_data[:3] == b'ID3':
                        ver = id3_data[3]
                        return parse_id3_apic_data(id3_data[10:], ver)
                    return None
                else:
                    f.seek(clen + (clen % 2), 1)
    except Exception:
        pass
    return None


def extract_wma_artwork(file_path):
    """Extract embedded WM/Picture artwork from WMA / ASF files."""
    try:
        with open(file_path, 'rb') as f:
            data = f.read(1024 * 1024 * 4)
            marker = 'WM/Picture'.encode('utf-16le')
            idx = data.find(marker)
            if idx != -1:
                sub = data[idx + len(marker) : idx + len(marker) + 1200]
                for magic in (b'\xff\xd8\xff', b'\x89PNG', b'GIF8'):
                    m_idx = sub.find(magic)
                    if m_idx != -1:
                        return data[idx + len(marker) + m_idx :]
    except Exception:
        pass
    return None


def find_folder_artwork(media_path):
    """
    Find dedicated album artwork in the media file's folder.
    NOTE: Never matches loose files by stem name to prevent accidental artwork hijacking.
    Ignores common mixed folders (Downloads, Desktop, Documents, etc.).
    """
    try:
        p = Path(media_path)
        if not p.is_file():
            return None
        folder = p.parent
        # Avoid common unorganized folders
        folder_name = folder.name.lower()
        if folder_name in {'downloads', 'desktop', 'documents', 'temp', 'tmp', ''} or folder.parent == folder:
            return None

        # Standard album art filenames only
        for name in ('cover.jpg', 'cover.png', 'folder.jpg', 'folder.png', 'albumart.jpg', 'front.jpg'):
            target = folder / name
            if target.is_file():
                return str(target)
    except Exception:
        pass
    return None


def round_pixmap(src, size=140, radius=8):
    """Scale, center-crop, and clip a QPixmap with smooth antialiased rounded corners."""
    if src.isNull():
        return src
    scaled = src.scaled(
        size, size,
        Qt.AspectRatioMode.KeepAspectRatioByExpanding,
        Qt.TransformationMode.SmoothTransformation
    )
    x = max(0, (scaled.width() - size) // 2)
    y = max(0, (scaled.height() - size) // 2)
    cropped = scaled.copy(x, y, size, size)

    out = QPixmap(size, size)
    out.fill(Qt.GlobalColor.transparent)
    p = QPainter(out)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    path = QPainterPath()
    path.addRoundedRect(QRectF(0, 0, size, size), radius, radius)
    p.setClipPath(path)
    p.drawPixmap(0, 0, cropped)
    p.setClipping(False)
    p.setPen(QPen(QColor(255, 255, 255, 25), 1))
    p.drawPath(path)
    p.end()
    return out


def fallback_colors(accent, is_light):
    """Flat accent-tinted surface and an icon with at least 4.5:1 contrast."""
    tint = QColor(accent)
    if not tint.isValid():
        tint = QColor('#0078d4')
    base = QColor('#f4f4f4' if is_light else '#242424')

    def blend(first, second, amount):
        return QColor(*[round(a * (1 - amount) + b * amount)
                        for a, b in zip(first.getRgb()[:3], second.getRgb()[:3])])

    def luminance(color):
        channels = [v / 255 for v in color.getRgb()[:3]]
        linear = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in channels]
        return sum(v * weight for v, weight in zip(linear, (.2126, .7152, .0722)))

    surface = blend(base, tint, .10 if is_light else .16)
    ink = QColor(tint)
    target = QColor('#000000' if is_light else '#ffffff')
    for step in range(21):
        ink = blend(tint, target, step / 20)
        low, high = sorted((luminance(surface), luminance(ink)))
        if (high + .05) / (low + .05) >= 4.5:
            break
    return surface, ink


def create_fallback_artwork(kind='Music', size=140, radius=8, accent=None, is_light=None):
    """Generate a flat, theme-aware artwork tile without a circular backdrop."""
    if is_light is None:
        is_light = _ACTIVE_IS_LIGHT if _ACTIVE_IS_LIGHT is not None else is_windows_light_theme()
    if accent is None:
        accent = _ACTIVE_ACCENT
    if accent is None:
        palette = get_windows_accent_palette(is_light)
        accent = palette.get('accent', '#0078d4' if is_light else '#60cdff')

    pix = QPixmap(size, size)
    pix.fill(Qt.GlobalColor.transparent)
    p = QPainter(pix)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)

    surface, ink = fallback_colors(accent, is_light)
    path = QPainterPath()
    path.addRoundedRect(QRectF(1, 1, size - 2, size - 2), radius, radius)
    p.fillPath(path, surface)

    # Center vector icon
    icon_name = 'video' if kind == 'Video' else ('stream' if kind == 'Stream' else 'music')
    icon_size = max(20, int(size * 0.58))
    icon = get_icon(icon_name, ink.name(), icon_size)
    i_rect = QRect((size - icon_size) // 2, (size - icon_size) // 2, icon_size, icon_size)
    icon.paint(p, i_rect)

    # Subtle border
    border_col = QColor(ink)
    border_col.setAlpha(30)
    p.setPen(QPen(border_col, 1))
    p.setBrush(Qt.BrushStyle.NoBrush)
    p.drawPath(path)
    p.end()
    return pix


def clear_artwork_cache():
    """Clear cached artwork pixmaps, e.g. when system accent or light/dark theme changes."""
    _ART_CACHE.clear()


def get_media_artwork(file_path_or_url, kind='Music', size=140, radius=8, is_light=None, accent=None):
    """
    Get cached or freshly extracted/generated QPixmap artwork for a media item.
    - Music: Strictly extracts genuine assigned embedded artwork (ID3 APIC, FLAC, M4A, OGG).
      Never shows application icons (VLC cone or document icon), and never hijacks random images by stem name.
    - Video: Extracts real video frame thumbnail via Windows Shell (thumbnail only, never app icon).
    - Fallback: Clean Windows 11 Fluent card with vector media icon in accent color (supports light/dark).
    """
    if is_light is None:
        is_light = _ACTIVE_IS_LIGHT if _ACTIVE_IS_LIGHT is not None else is_windows_light_theme()
    if accent is None:
        accent = _ACTIVE_ACCENT
    if accent is None:
        palette = get_windows_accent_palette(is_light)
        accent = palette.get('accent', '#0078d4' if is_light else '#60cdff')

    key = (str(file_path_or_url), size, radius, str(accent).lower() if accent else None, bool(is_light))
    if key in _ART_CACHE:
        return _ART_CACHE[key]

    path_str = str(file_path_or_url)
    ext = Path(path_str).suffix.lower() if '://' not in path_str else ''

    # 1. For Video: Windows Shell real thumbnail frame (strictly thumbnail only, never icon)
    if kind == 'Video':
        win_thumb = extract_windows_thumbnail(path_str, size)
        if win_thumb and not win_thumb.isNull():
            out = round_pixmap(win_thumb, size, radius)
            _ART_CACHE[key] = out
            return out

        raw_img = extract_mp4_artwork(path_str)
        if raw_img:
            pm = QPixmap()
            if pm.loadFromData(raw_img) and not pm.isNull():
                out = round_pixmap(pm, size, radius)
                _ART_CACHE[key] = out
                return out

    # 2. For Music: Strictly extract assigned embedded tags
    elif kind == 'Music':
        raw_img = None
        if ext == '.mp3':
            raw_img = extract_id3_artwork(path_str)
        elif ext == '.flac':
            raw_img = extract_flac_artwork(path_str)
        elif ext in ('.m4a', '.mp4', '.aac', '.m4b'):
            raw_img = extract_mp4_artwork(path_str)
        elif ext in ('.ogg', '.opus'):
            raw_img = extract_ogg_artwork(path_str)
        elif ext == '.wav':
            raw_img = extract_wav_artwork(path_str)
        elif ext == '.wma':
            raw_img = extract_wma_artwork(path_str)

        if raw_img:
            pm = QPixmap()
            if pm.loadFromData(raw_img) and not pm.isNull():
                out = round_pixmap(pm, size, radius)
                _ART_CACHE[key] = out
                return out

        # Dedicated album art file in specific album folders
        folder_art = find_folder_artwork(path_str)
        if folder_art:
            pm = QPixmap(folder_art)
            if not pm.isNull():
                out = round_pixmap(pm, size, radius)
                _ART_CACHE[key] = out
                return out

    # 3. Fallback Fluent design artwork card (never an app icon or traffic cone)
    out = create_fallback_artwork(kind, size, radius, accent, is_light)
    _ART_CACHE[key] = out
    return out
