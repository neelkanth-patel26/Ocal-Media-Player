import tempfile
import unittest
from pathlib import Path
from PySide6.QtWidgets import QApplication

from src.library import Library
from src.app import PlayerWindow

app = QApplication.instance() or QApplication([])


class TestSelection(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.lib = Library(self.root / 'data')
        # Create 3 dummy media files
        self.f1 = self.root / 'track1.mp3'
        self.f1.touch()
        self.f2 = self.root / 'track2.mp3'
        self.f2.touch()
        self.f3 = self.root / 'track3.mp3'
        self.f3.touch()
        self.lib.add([self.f1, self.f2, self.f3])

    def tearDown(self):
        self.temp.cleanup()

    def test_active_selection_updates_on_playback(self):
        window = PlayerWindow(self.lib)
        self.assertEqual(len(window.visible_items), 3)

        # Initially play track 2
        window.play_item(window.visible_items[1])
        selected_rows = [index.row() for index in window.table.selectionModel().selectedRows()]
        self.assertEqual(selected_rows, [1])

        # Next play track 0 (simulating shuffle or next)
        window.play_item(window.visible_items[0])
        selected_rows = [index.row() for index in window.table.selectionModel().selectedRows()]
        self.assertEqual(selected_rows, [0])

        # Play track 2
        window.play_item(window.visible_items[2])
        selected_rows = [index.row() for index in window.table.selectionModel().selectedRows()]
        self.assertEqual(selected_rows, [2])
        window.close()


if __name__ == '__main__':
    unittest.main()

