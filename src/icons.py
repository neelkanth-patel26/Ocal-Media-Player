"""Fluent Icon Pack generator for Ocal Media Player.
Renders official Windows 11 Segoe Fluent Icons with pure QPainter vector fallbacks.
"""
from pathlib import Path
from PySide6.QtGui import (
    QIcon, QPixmap, QPainter, QColor, QPen, QBrush, QPainterPath, QFont, QFontDatabase
)
from PySide6.QtCore import Qt, QRect, QRectF, QPointF

_CACHE = {}
_FONT_FAMILY = None


def _init_font():
    global _FONT_FAMILY
    if _FONT_FAMILY is not None:
        return _FONT_FAMILY

    # Try bundled font first
    font_path = Path(__file__).resolve().parent.parent / 'assets' / 'SegoeFluentIcons.ttf'
    if font_path.is_file():
        fid = QFontDatabase.addApplicationFont(str(font_path))
        if fid != -1:
            fams = QFontDatabase.applicationFontFamilies(fid)
            if fams:
                _FONT_FAMILY = fams[0]
                return _FONT_FAMILY

    # Fall back to installed system families
    available = QFontDatabase.families()
    if 'Segoe Fluent Icons' in available:
        _FONT_FAMILY = 'Segoe Fluent Icons'
    elif 'Segoe MDL2 Assets' in available:
        _FONT_FAMILY = 'Segoe MDL2 Assets'
    else:
        _FONT_FAMILY = ''
    return _FONT_FAMILY


FLUENT_GLYPHS = {
    'home': '\uE80F',
    'arrow_left': '\uE72B',
    'back': '\uE72B',
    'music': '\uEC4F',
    'video': '\uE714',
    'heart_outline': '\uEB51',
    'heart_fill': '\uEB52',
    'history': '\uE81C',
    'nowplaying': '\uE768',
    'keyboard': '\uE765',
    'info': '\uE946',
    'open_files': '\uE8E5',
    'open_file': '\uE8E5',
    'folder': '\uED25',
    'stream': '\uE774',
    'shuffle': '\uE8B1',
    'repeat': '\uE8EE',
    'refresh': '\uE72C',
    'prev': '\uE892',
    'next': '\uE893',
    'play': '\uE768',
    'pause': '\uE769',
    'volume': '\uE767',
    'vol_high': '\uE767',
    'vol_mid': '\uE994',
    'vol_low': '\uE993',
    'mute': '\uE74F',
    'vol_mute': '\uE74F',
    'fullscreen': '\uE740',
    'restore': '\uE73F',
    'more': '\uE712',
    'bookmark': '\uE734',
    'subtitles': '\uED1E',
    'camera': '\uE722',
    'cap_min': '\uE921',
    'cap_max': '\uE922',
    'cap_restore': '\uE923',
    'cap_close': '\uE8BB',
    'view_list': '\uEA37',
    'view_grid': '\uF0E2',
    'settings': '\uE713',
    'gear': '\uE713',
    'check': '\uE73E',
    'download': '\uE896',
    'palette': '\uE790',
    'search': '\uE721',
}


def get_icon(name, color='#ffffff', size=24):
    """Return a cached QIcon rendered via the Segoe Fluent Icon pack."""
    key = (name, color, size)
    if key in _CACHE:
        return _CACHE[key]

    fam = _init_font()
    pix = QPixmap(size, size)
    pix.fill(Qt.GlobalColor.transparent)
    p = QPainter(pix)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.setRenderHint(QPainter.RenderHint.TextAntialiasing)

    # If the glyph is in Fluent Icon Pack and font is available
    if fam and name in FLUENT_GLYPHS:
        char = FLUENT_GLYPHS[name]
        pixel_size = max(9, int(size * 0.68))
        f = QFont(fam)
        f.setPixelSize(pixel_size)
        f.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
        p.setFont(f)
        p.setPen(QColor(color))
        p.drawText(QRect(0, 0, size, size), Qt.AlignmentFlag.AlignCenter, char)
        p.end()
        icon = QIcon(pix)
        _CACHE[key] = icon
        return icon

    # Specialized rendering for back10 / fwd10 with numeric overlay
    if name in {'back10', 'fwd10'}:
        scale = size / 24.0
        p.scale(scale, scale)
        pen = QPen(QColor(color), 1.6, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
        p.setPen(pen)
        if name == 'back10':
            p.drawArc(QRectF(4, 4, 16, 16), 45 * 16, 270 * 16)
            p.drawLine(12.5, 3.2, 15.5, 4.8)
            p.drawLine(15.5, 4.8, 13.8, 8)
        else:
            p.drawArc(QRectF(4, 4, 16, 16), -45 * 16, -270 * 16)
            p.drawLine(11.5, 3.2, 8.5, 4.8)
            p.drawLine(8.5, 4.8, 10.2, 8)
        f = QFont('Segoe UI Variable Display', 6, QFont.Weight.Bold)
        p.setFont(f)
        p.drawText(QRectF(5, 7, 14, 11), Qt.AlignmentFlag.AlignCenter, '10')
        p.end()
        icon = QIcon(pix)
        _CACHE[key] = icon
        return icon

    # Vector path fallback for any unmapped symbols
    scale = size / 24.0
    p.scale(scale, scale)
    pen = QPen(QColor(color), 1.6, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
    p.setPen(pen)
    brush = QBrush(QColor(color))

    if name == 'home':
        path = QPainterPath()
        path.moveTo(4, 11)
        path.lineTo(12, 4.5)
        path.lineTo(20, 11)
        path.lineTo(17.5, 11)
        path.lineTo(17.5, 19)
        path.lineTo(6.5, 19)
        path.lineTo(6.5, 11)
        path.closeSubpath()
        p.drawPath(path)
    elif name in {'arrow_left', 'back'}:
        p.drawLine(6, 12, 18, 12)
        p.drawLine(6, 12, 11, 7)
        p.drawLine(6, 12, 11, 17)
    elif name == 'music':
        p.setBrush(brush)
        p.drawEllipse(QRectF(5, 13.5, 5, 4))
        p.drawEllipse(QRectF(14, 11.5, 5, 4))
        p.drawLine(10, 15, 10, 5.5)
        p.drawLine(19, 13, 19, 4)
        p.drawLine(10, 5.5, 19, 4)
        p.drawLine(10, 7.5, 19, 6)
    elif name == 'video':
        p.drawRoundedRect(QRectF(4, 5, 16, 14), 2.5, 2.5)
        p.setBrush(brush)
        path = QPainterPath()
        path.moveTo(10, 8.5)
        path.lineTo(15.5, 12)
        path.lineTo(10, 15.5)
        path.closeSubpath()
        p.drawPath(path)
    elif name == 'play':
        p.setBrush(brush)
        path = QPainterPath()
        path.moveTo(8.5, 6)
        path.lineTo(18, 12)
        path.lineTo(8.5, 18)
        path.closeSubpath()
        p.drawPath(path)
    elif name == 'pause':
        p.setBrush(brush)
        p.drawRoundedRect(QRectF(7, 6, 3.5, 12), 1, 1)
        p.drawRoundedRect(QRectF(13.5, 6, 3.5, 12), 1, 1)

    p.end()
    icon = QIcon(pix)
    _CACHE[key] = icon
    return icon
