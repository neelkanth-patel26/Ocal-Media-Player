import tempfile
import unittest
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QPixmap, QImage

from src.artwork import (
    create_fallback_artwork, round_pixmap, get_media_artwork,
    extract_windows_thumbnail, extract_id3_artwork, find_folder_artwork,
    _ART_CACHE
)

app = QApplication.instance() or QApplication([])


class TestArtwork(unittest.TestCase):
    def test_fallback_artwork(self):
        pm_music = create_fallback_artwork('Music', 140, 8)
        self.assertFalse(pm_music.isNull())
        self.assertEqual(pm_music.size(), QSize(140, 140))

        pm_video = create_fallback_artwork('Video', 64, 4)
        self.assertFalse(pm_video.isNull())
        self.assertEqual(pm_video.size(), QSize(64, 64))

        pm_stream = create_fallback_artwork('Stream', 32, 4)
        self.assertFalse(pm_stream.isNull())
        self.assertEqual(pm_stream.size(), QSize(32, 32))

    def test_round_pixmap(self):
        src = QPixmap(100, 100)
        src.fill()
        rounded = round_pixmap(src, size=50, radius=6)
        self.assertFalse(rounded.isNull())
        self.assertEqual(rounded.size(), QSize(50, 50))

    def test_get_media_artwork_caching(self):
        _ART_CACHE.clear()
        art1 = get_media_artwork('test_virtual_track.mp3', 'Music', 140, 8)
        self.assertFalse(art1.isNull())
        self.assertIn(('test_virtual_track.mp3', 140, 8), _ART_CACHE)

        art2 = get_media_artwork('test_virtual_track.mp3', 'Music', 140, 8)
        self.assertEqual(art1, art2)

    def test_no_stem_name_artwork_hijacking(self):
        """Verify that an image with the same name as the song is NOT hijacked as artwork."""
        with tempfile.TemporaryDirectory() as td:
            tdp = Path(td)
            mp3_path = tdp / 'Demo.mp3'
            # Write a dummy MP3 without ID3 tags
            mp3_path.write_bytes(b'\xff\xfb\x90\x00' + b'\x00' * 500)

            # Write an image with the exact same stem name
            jpg_path = tdp / 'Demo.jpg'
            qimg = QImage(120, 120, QImage.Format.Format_RGB32)
            qimg.fill(Qt.GlobalColor.red)
            qimg.save(str(jpg_path))

            _ART_CACHE.clear()
            art = get_media_artwork(str(mp3_path), 'Music', 140, 8)
            # Should NOT return Demo.jpg, should fall back to player card
            self.assertFalse(art.isNull())
            # find_folder_artwork must return None for Demo.mp3
            self.assertIsNone(find_folder_artwork(str(mp3_path)))

    def test_music_without_embedded_art_never_returns_app_icon(self):
        """Verify that audio without embedded tags falls back to player card, never an app icon."""
        with tempfile.TemporaryDirectory() as td:
            tdp = Path(td)
            wav_path = tdp / 'no_art.wav'
            wav_path.write_bytes(b'RIFF$\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00D\xac\x00\x00\x88X\x01\x00\x02\x00\x10\x00data\x00\x00\x00\x00')

            _ART_CACHE.clear()
            art = get_media_artwork(str(wav_path), 'Music', 140, 8)
            self.assertFalse(art.isNull())
            # Windows shell thumbnail with SIIGBF_THUMBNAILONLY must return None for audio with no art
            self.assertIsNone(extract_windows_thumbnail(str(wav_path), 140))

    def test_embedded_id3_apic_extraction(self):
        """Verify that embedded ID3v2 APIC artwork is extracted correctly."""
        with tempfile.TemporaryDirectory() as td:
            tdp = Path(td)
            # Generate a real 20x20 JPEG
            qimg = QImage(20, 20, QImage.Format.Format_RGB32)
            qimg.fill(Qt.GlobalColor.blue)
            raw_jpg_path = tdp / 'raw.jpg'
            qimg.save(str(raw_jpg_path), 'JPEG')
            jpg_bytes = raw_jpg_path.read_bytes()

            # Build ID3v2.3 tag with APIC frame
            mime = b'image/jpeg\x00'
            pic_type = b'\x03'  # Cover (front)
            desc = b'front\x00'
            apic_payload = b'\x00' + mime + pic_type + desc + jpg_bytes
            apic_header = b'APIC' + len(apic_payload).to_bytes(4, 'big') + b'\x00\x00'

            tag_payload = apic_header + apic_payload
            tag_size = len(tag_payload)
            # Synchsafe size
            s_size = (
                ((tag_size >> 21) & 0x7F).to_bytes(1, 'big')
                + ((tag_size >> 14) & 0x7F).to_bytes(1, 'big')
                + ((tag_size >> 7) & 0x7F).to_bytes(1, 'big')
                + (tag_size & 0x7F).to_bytes(1, 'big')
            )
            id3_header = b'ID3\x03\x00\x00' + s_size

            mp3_path = tdp / 'tagged.mp3'
            mp3_path.write_bytes(id3_header + tag_payload + b'\xff\xfb\x90\x00' + b'\x00' * 500)

            extracted = extract_id3_artwork(str(mp3_path))
            self.assertIsNotNone(extracted)
            self.assertEqual(extracted[:3], b'\xff\xd8\xff')

            _ART_CACHE.clear()
            art = get_media_artwork(str(mp3_path), 'Music', 140, 8)
            self.assertFalse(art.isNull())

    def test_windows_shell_thumbnail(self):
        preview_file = Path('assets/player-preview.png').resolve()
        if preview_file.is_file():
            pm = extract_windows_thumbnail(str(preview_file), size=96)
            self.assertIsNotNone(pm)
            self.assertFalse(pm.isNull())


if __name__ == '__main__':
    unittest.main()
