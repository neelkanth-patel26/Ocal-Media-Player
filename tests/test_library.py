import json
import tempfile
import unittest
from pathlib import Path
from src.library import Library, clock


class LibraryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.lib = Library(self.root / 'data')

    def tearDown(self):
        self.temp.cleanup()

    def test_import_deduplicates_and_rejects_missing_or_unsupported(self):
        track = self.root / 'Music 音楽.wav'
        track.touch()
        self.lib.add([track, track, self.root / 'missing.wav', 'javascript:alert(1)'])
        self.assertEqual(len(self.lib.items), 1)
        self.assertEqual(self.lib.items[0]['kind'], 'Music')

    def test_persistence_of_bookmarks_resume_and_favorites(self):
        entry = self.lib.add(['https://example.com/stream'])[0]
        entry.update(favorite=True, position=16000, duration=90000, bookmarks=[{'name': 'Verse', 'time': 23000}])
        self.lib.save()
        restored = Library(self.lib.directory)
        self.assertEqual(restored.items, self.lib.items)

    def test_corruption_preserved(self):
        self.lib.path.write_text('{bad json', encoding='utf-8')
        restored = Library(self.lib.directory)
        self.assertTrue(restored.warning)
        restored.save()
        self.assertEqual((self.lib.directory / 'library.recovery.json').read_text(), '{bad json')

    def test_clock(self):
        self.assertEqual(clock(3_661_000), '1:01:01')
        self.assertEqual(clock(-1), '0:00')


if __name__ == '__main__':
    unittest.main()
