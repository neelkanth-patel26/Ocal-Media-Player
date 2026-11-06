import unittest
import struct
import tempfile
from pathlib import Path
from src.metadata import extract_media_metadata, _parse_id3_tags, _get_wav_duration


class TestMetadata(unittest.TestCase):
    def test_wav_duration(self):
        # Create a synthetic WAV header for 2 seconds of 44100Hz 16-bit stereo (byte_rate = 176400)
        byte_rate = 176400
        data_size = byte_rate * 2  # 2 seconds -> 2000 ms
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            # RIFF header
            f.write(b'RIFF')
            f.write(struct.pack('<I', 36 + data_size))
            f.write(b'WAVE')
            # fmt chunk
            f.write(b'fmt ')
            f.write(struct.pack('<I', 16))  # chunk size
            f.write(struct.pack('<H', 1))   # PCM format
            f.write(struct.pack('<H', 2))   # 2 channels
            f.write(struct.pack('<I', 44100)) # sample rate
            f.write(struct.pack('<I', byte_rate)) # byte rate
            f.write(struct.pack('<H', 4))   # block align
            f.write(struct.pack('<H', 16))  # bits per sample
            # data chunk
            f.write(b'data')
            f.write(struct.pack('<I', data_size))
            f.write(b'\x00' * 100) # dummy payload
            tmp_path = f.name

        try:
            dur, tags = extract_media_metadata(tmp_path)
            self.assertEqual(dur, 2000)
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    def test_id3_tag_parsing(self):
        # Construct small ID3v2.3 header with TLEN (duration: "185000") and TPE1 (artist: "Artist Name")
        tlen_payload = b'\x00185000'
        tpe1_payload = b'\x00Test Artist'
        frame_tlen = b'TLEN' + struct.pack('>I', len(tlen_payload)) + b'\x00\x00' + tlen_payload
        frame_tpe1 = b'TPE1' + struct.pack('>I', len(tpe1_payload)) + b'\x00\x00' + tpe1_payload
        frames = frame_tlen + frame_tpe1
        tag_size = len(frames)
        # ID3 synchsafe size: 4 bytes where high bit is 0
        b3 = tag_size & 0x7F
        b2 = (tag_size >> 7) & 0x7F
        b1 = (tag_size >> 14) & 0x7F
        b0 = (tag_size >> 21) & 0x7F
        id3_header = b'ID3\x03\x00\x00' + bytes([b0, b1, b2, b3]) + frames

        tags, total_size = _parse_id3_tags(id3_header)
        self.assertEqual(tags['duration'], 185000)
        self.assertEqual(tags['artist'], 'Test Artist')


if __name__ == '__main__':
    unittest.main()

