"""Lightweight, zero-dependency pure Python audio/video metadata & duration extraction."""
import struct
from pathlib import Path


def _parse_id3_tags(data):
    """Extract TLEN, TPE1 (artist), TALB (album), TIT2 (title) from ID3v2 header bytes."""
    tags = {'duration': 0, 'artist': '', 'album': '', 'title': ''}
    if len(data) < 10 or data[:3] != b'ID3':
        return tags, 0

    version = data[3]
    tag_size = (
        ((data[6] & 0x7F) << 21)
        | ((data[7] & 0x7F) << 14)
        | ((data[8] & 0x7F) << 7)
        | (data[9] & 0x7F)
    )
    total_tag_size = tag_size + 10

    pos = 10
    limit = min(len(data), total_tag_size)
    while pos + 10 < limit:
        if version in (3, 4):
            frame_id = data[pos : pos + 4]
            if frame_id == b'\x00\x00\x00\x00':
                break
            if version == 4:
                frame_len = (
                    ((data[pos + 4] & 0x7F) << 21)
                    | ((data[pos + 5] & 0x7F) << 14)
                    | ((data[pos + 6] & 0x7F) << 7)
                    | (data[pos + 7] & 0x7F)
                )
            else:
                frame_len = int.from_bytes(data[pos + 4 : pos + 8], 'big')
            pos += 10
            if frame_len > 0 and pos + frame_len <= len(data):
                content = data[pos : pos + frame_len]
                if frame_id in (b'TLEN', b'TPE1', b'TALB', b'TIT2'):
                    text = _decode_id3_text(content)
                    if frame_id == b'TLEN':
                        try:
                            tags['duration'] = int(text.strip())
                        except (ValueError, TypeError):
                            pass
                    elif frame_id == b'TPE1':
                        tags['artist'] = text
                    elif frame_id == b'TALB':
                        tags['album'] = text
                    elif frame_id == b'TIT2':
                        tags['title'] = text
            pos += frame_len
        elif version == 2:
            frame_id = data[pos : pos + 3]
            if frame_id == b'\x00\x00\x00':
                break
            frame_len = int.from_bytes(data[pos + 3 : pos + 6], 'big')
            pos += 6
            if frame_len > 0 and pos + frame_len <= len(data):
                content = data[pos : pos + frame_len]
                if frame_id in (b'TLE', b'TP1', b'TAL', b'TT2'):
                    text = _decode_id3_text(content)
                    if frame_id == b'TLE':
                        try:
                            tags['duration'] = int(text.strip())
                        except (ValueError, TypeError):
                            pass
                    elif frame_id == b'TP1':
                        tags['artist'] = text
                    elif frame_id == b'TAL':
                        tags['album'] = text
                    elif frame_id == b'TT2':
                        tags['title'] = text
            pos += frame_len
        else:
            break

    return tags, total_tag_size


def _decode_id3_text(frame_bytes):
    """Decode text frame considering ID3 encoding byte."""
    if not frame_bytes:
        return ''
    enc = frame_bytes[0]
    payload = frame_bytes[1:]
    try:
        if enc == 0:
            return payload.split(b'\x00')[0].decode('latin-1', errors='ignore').strip()
        elif enc in (1, 2):
            text = payload.decode('utf-16', errors='ignore').split('\x00')[0]
            return text.strip()
        elif enc == 3:
            return payload.split(b'\x00')[0].decode('utf-8', errors='ignore').strip()
    except Exception:
        pass
    return ''


MPEG_BITRATES = {
    # (version, layer): [bitrates for index 0..14] in kbps
    (1, 1): [0, 32, 64, 96, 128, 160, 192, 224, 256, 288, 320, 352, 384, 416, 448],
    (1, 2): [0, 32, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320, 384],
    (1, 3): [0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320],
    (2, 1): [0, 32, 48, 56, 64, 80, 96, 112, 128, 144, 160, 176, 192, 224, 256],
    (2, 2): [0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160],
    (2, 3): [0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160],
}

MPEG_SAMPLERATES = {
    1: [44100, 48000, 32000],
    2: [22050, 24000, 16000],
    2.5: [11025, 12000, 8000],
}


def _get_mp3_duration(file_path, file_size):
    """Estimate or accurately calculate MP3 duration in ms."""
    try:
        with open(file_path, 'rb') as f:
            head = f.read(1024 * 512)  # Read up to 512KB for headers
        if not head:
            return 0, {}

        tags, id3_size = _parse_id3_tags(head)
        if tags['duration'] > 1000:
            return tags['duration'], tags

        audio_data = head[id3_size:]
        idx = 0
        while idx + 4 < len(audio_data):
            b0 = audio_data[idx]
            b1 = audio_data[idx + 1]
            if b0 == 0xFF and (b1 & 0xE0) == 0xE0:
                ver_bits = (b1 >> 3) & 0x03
                ver = 1 if ver_bits == 3 else (2 if ver_bits == 2 else 2.5) if ver_bits == 0 else None
                layer_bits = (b1 >> 1) & 0x03
                layer = 3 if layer_bits == 1 else (2 if layer_bits == 2 else 1 if layer_bits == 3 else None)
                if ver is not None and layer is not None:
                    b2 = audio_data[idx + 2]
                    br_idx = (b2 >> 4) & 0x0F
                    sr_idx = (b2 >> 2) & 0x03
                    chan_mode = (audio_data[idx + 3] >> 6) & 0x03
                    is_mono = chan_mode == 3

                    v_key = 1 if ver == 1 else 2
                    rates = MPEG_BITRATES.get((v_key, layer))
                    samplerates = MPEG_SAMPLERATES.get(ver)
                    if rates and samplerates and 0 < br_idx < len(rates) and sr_idx < len(samplerates):
                        bitrate = rates[br_idx]
                        sample_rate = samplerates[sr_idx]

                        # Check Xing / Info header
                        side_info_len = (17 if is_mono else 32) if ver == 1 else (9 if is_mono else 17)
                        xing_offset = idx + 4 + side_info_len
                        if xing_offset + 12 < len(audio_data):
                            tag = audio_data[xing_offset : xing_offset + 4]
                            if tag in (b'Xing', b'Info'):
                                flags = int.from_bytes(audio_data[xing_offset + 4 : xing_offset + 8], 'big')
                                if flags & 0x01:  # frames field present
                                    total_frames = int.from_bytes(audio_data[xing_offset + 8 : xing_offset + 12], 'big')
                                    samples_per_frame = 384 if layer == 1 else (1152 if ver == 1 else 576)
                                    dur_ms = int(total_frames * samples_per_frame * 1000 / sample_rate)
                                    if dur_ms > 0:
                                        return dur_ms, tags

                        # Check VBRI header (always at offset 32 after header)
                        vbri_offset = idx + 4 + 32
                        if vbri_offset + 26 < len(audio_data) and audio_data[vbri_offset : vbri_offset + 4] == b'VBRI':
                            total_frames = int.from_bytes(audio_data[vbri_offset + 14 : vbri_offset + 18], 'big')
                            dur_ms = int(total_frames * 1152 * 1000 / sample_rate)
                            if dur_ms > 0:
                                return dur_ms, tags

                        # Fallback: CBR estimation from file size and bitrate
                        audio_len = max(0, file_size - id3_size)
                        cbr_dur = int(audio_len * 8 * 1000 / (bitrate * 1000))
                        return cbr_dur, tags
            idx += 1
        return tags['duration'], tags
    except Exception:
        return 0, {}


def _get_flac_metadata(file_path):
    """Extract exact duration and tags from FLAC STREAMINFO & VORBIS_COMMENT."""
    tags = {'duration': 0, 'artist': '', 'album': '', 'title': ''}
    try:
        with open(file_path, 'rb') as f:
            if f.read(4) != b'fLaC':
                return 0, tags
            while True:
                head = f.read(4)
                if len(head) < 4:
                    break
                is_last = head[0] & 0x80
                block_type = head[0] & 0x7F
                block_len = int.from_bytes(head[1:4], 'big')
                data = f.read(block_len)
                if block_type == 0 and len(data) >= 34:  # STREAMINFO
                    b10, b11, b12, b13, b14, b15, b16, b17 = data[10:18]
                    sample_rate = (b10 << 12) | (b11 << 4) | (b12 >> 4)
                    total_samples = ((b13 & 0x0F) << 32) | (b14 << 24) | (b15 << 16) | (b16 << 8) | b17
                    if sample_rate > 0 and total_samples > 0:
                        tags['duration'] = int(total_samples * 1000 // sample_rate)
                elif block_type == 4:  # VORBIS_COMMENT
                    try:
                        pos = 0
                        vendor_len = int.from_bytes(data[pos : pos + 4], 'little')
                        pos += 4 + vendor_len
                        comment_count = int.from_bytes(data[pos : pos + 4], 'little')
                        pos += 4
                        for _ in range(min(comment_count, 100)):
                            if pos + 4 > len(data):
                                break
                            c_len = int.from_bytes(data[pos : pos + 4], 'little')
                            pos += 4
                            if pos + c_len <= len(data):
                                comment = data[pos : pos + c_len].decode('utf-8', errors='ignore')
                                if '=' in comment:
                                    k, v = comment.split('=', 1)
                                    k_lower = k.lower()
                                    if k_lower == 'artist' and not tags['artist']:
                                        tags['artist'] = v.strip()
                                    elif k_lower == 'album' and not tags['album']:
                                        tags['album'] = v.strip()
                                    elif k_lower == 'title' and not tags['title']:
                                        tags['title'] = v.strip()
                            pos += c_len
                    except Exception:
                        pass
                if is_last:
                    break
        return tags['duration'], tags
    except Exception:
        return 0, tags


def _get_wav_duration(file_path):
    """Extract exact duration from WAV header."""
    tags = {'duration': 0, 'artist': '', 'album': '', 'title': ''}
    try:
        with open(file_path, 'rb') as f:
            riff = f.read(12)
            if len(riff) < 12 or riff[:4] != b'RIFF' or riff[8:12] != b'WAVE':
                return 0, tags
            byte_rate = 0
            data_size = 0
            while True:
                chunk_header = f.read(8)
                if len(chunk_header) < 8:
                    break
                cid, csize = chunk_header[:4], int.from_bytes(chunk_header[4:8], 'little')
                if cid == b'fmt ' and csize >= 16:
                    fmt_data = f.read(csize)
                    byte_rate = int.from_bytes(fmt_data[8:12], 'little')
                elif cid == b'data':
                    data_size = csize
                    f.seek(csize, 1)
                else:
                    f.seek(csize, 1)
                if byte_rate > 0 and data_size > 0:
                    tags['duration'] = int(data_size * 1000 // byte_rate)
                    return tags['duration'], tags
        return tags['duration'], tags
    except Exception:
        return 0, tags


def _get_mp4_metadata(file_path):
    """Extract duration and tags from M4A / MP4 / MOV mvhd atom."""
    tags = {'duration': 0, 'artist': '', 'album': '', 'title': ''}
    try:
        with open(file_path, 'rb') as f:
            buf = f.read(1024 * 1024 * 8)  # Read up to 8MB
            mvhd_idx = buf.find(b'mvhd')
            if mvhd_idx != -1 and mvhd_idx >= 4:
                pos = mvhd_idx + 4
                version = buf[pos]
                if version == 0:
                    timescale = int.from_bytes(buf[pos + 12 : pos + 16], 'big')
                    dur = int.from_bytes(buf[pos + 16 : pos + 20], 'big')
                else:
                    timescale = int.from_bytes(buf[pos + 20 : pos + 24], 'big')
                    dur = int.from_bytes(buf[pos + 24 : pos + 32], 'big')
                if timescale > 0:
                    tags['duration'] = int(dur * 1000 // timescale)

            # Look for basic artist / album atoms
            for atom_name, key in ((b'\xa9ART', 'artist'), (b'aART', 'artist'), (b'\xa9alb', 'album'), (b'\xa9nam', 'title')):
                idx = buf.find(atom_name)
                if idx != -1:
                    data_idx = buf.find(b'data', idx)
                    if data_idx != -1 and data_idx - idx < 24:
                        len_bytes = buf[data_idx - 4 : data_idx]
                        atom_len = int.from_bytes(len_bytes, 'big')
                        val = buf[data_idx + 8 : data_idx - 4 + atom_len].decode('utf-8', errors='ignore').strip()
                        if val and not tags[key]:
                            tags[key] = val
        return tags['duration'], tags
    except Exception:
        return 0, tags


def _get_ogg_duration(file_path):
    """Extract duration from Ogg Vorbis/Opus file."""
    tags = {'duration': 0, 'artist': '', 'album': '', 'title': ''}
    try:
        with open(file_path, 'rb') as f:
            f.seek(0, 2)
            fsize = f.tell()
            read_size = min(fsize, 65536)
            f.seek(max(0, fsize - read_size))
            tail = f.read(read_size)
            idx = tail.rfind(b'OggS')
            if idx != -1 and idx + 14 <= len(tail):
                granule_pos = int.from_bytes(tail[idx + 6 : idx + 14], 'little')
                if granule_pos > 0:
                    # Default sample rate: Opus is 48000, Vorbis is commonly 44100
                    ext = Path(file_path).suffix.lower()
                    sr = 48000 if ext == '.opus' else 44100
                    tags['duration'] = int(granule_pos * 1000 // sr)
        return tags['duration'], tags
    except Exception:
        return 0, tags


def extract_media_metadata(file_path):
    """
    Extract duration (ms) and metadata tags (artist, album, title)
    for MP3, FLAC, WAV, M4A, MP4, MOV, OGG, OPUS.
    Returns (duration_ms, tags_dict).
    """
    p = Path(file_path)
    if not p.is_file():
        return 0, {}

    try:
        fsize = p.stat().st_size
    except OSError:
        return 0, {}

    ext = p.suffix.lower()
    if ext == '.mp3':
        return _get_mp3_duration(str(p), fsize)
    elif ext == '.flac':
        return _get_flac_metadata(str(p))
    elif ext == '.wav':
        return _get_wav_duration(str(p))
    elif ext in ('.m4a', '.mp4', '.mov', '.aac', '.m4v'):
        return _get_mp4_metadata(str(p))
    elif ext in ('.ogg', '.opus', '.oga'):
        return _get_ogg_duration(str(p))

    return 0, {}

