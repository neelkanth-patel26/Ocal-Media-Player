"""Tests for Video Watch Mode, sliding overlay drawers, and fullscreen experience."""
import unittest
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QPoint, QRect, QEvent
from PySide6.QtGui import QMouseEvent

from src.app import PlayerWindow
from src.library import Library
from src.engine import ROOT


class TestVideoWatchMode(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.library = Library(ROOT / '.test-data' / 'test-watch-lib')
        self.window = PlayerWindow(self.library)
        self.window.resize(1200, 800)
        self.window.show()
        self.app.processEvents()

    def tearDown(self):
        self.window.close()
        self.app.processEvents()

    def test_enter_and_exit_video_watch_mode(self):
        # Initial library mode
        self.assertFalse(self.window.is_video_mode)
        self.assertEqual(self.window.sidebar.parent(), self.window.canvas)
        self.assertEqual(self.window.queue_frame.parent(), self.window.canvas)
        self.assertEqual(self.window.transport.parent(), self.window.canvas)
        self.assertFalse(self.window.top_bar_widget.isHidden())
        self.assertTrue(self.window.video_top_bar.isHidden())

        # Enter video watch mode
        self.window.navigate('Now playing')
        self.app.processEvents()
        self.assertTrue(self.window.is_video_mode)
        self.assertEqual(self.window.sidebar.parent(), self.window.left_drawer)
        self.assertEqual(self.window.queue_frame.parent(), self.window.right_drawer)
        self.assertEqual(self.window.transport.parent(), self.window)
        self.assertTrue(self.window.top_bar_widget.isHidden())
        self.assertFalse(self.window.video_top_bar.isHidden())

        # Exit video watch mode back to library
        self.window.exit_video_to_library()
        self.app.processEvents()
        self.assertFalse(self.window.is_video_mode)
        self.assertEqual(self.window.sidebar.parent(), self.window.canvas)
        self.assertEqual(self.window.queue_frame.parent(), self.window.canvas)
        self.assertEqual(self.window.transport.parent(), self.window.canvas)
        self.assertFalse(self.window.top_bar_widget.isHidden())
        self.assertTrue(self.window.video_top_bar.isHidden())

    def test_sliding_drawers_on_edge_hover(self):
        self.window.navigate('Now playing')
        self.app.processEvents()
        w = self.window.width()
        h = self.window.height()

        # Sharp left edge hover
        self.window.open_left_drawer()
        self.assertTrue(self.window.left_drawer_open)
        self.window.app.processEvents() if hasattr(self.window, 'app') else self.app.processEvents()
        self.assertFalse(self.window.left_drawer.isHidden())

        # Close left drawer
        self.window.close_left_drawer()
        self.assertFalse(self.window.left_drawer_open)

        # Sharp right edge hover
        self.window.open_right_drawer()
        self.assertTrue(self.window.right_drawer_open)
        self.app.processEvents()
        self.assertFalse(self.window.right_drawer.isHidden())

        # Close right drawer
        self.window.close_right_drawer()
        self.assertFalse(self.window.right_drawer_open)

    def test_fullscreen_experience(self):
        self.window.navigate('Now playing')
        self.app.processEvents()

        # Enter fullscreen
        self.window.fullscreen()
        self.app.processEvents()
        self.assertTrue(self.window.isFullScreen())
        self.assertTrue(self.window.is_video_mode)

        # Exit fullscreen
        self.window.fullscreen()
        self.app.processEvents()
        self.assertFalse(self.window.isFullScreen())

    def test_wake_and_auto_hide_controls(self):
        self.window.navigate('Now playing')
        self.app.processEvents()

        # Wake controls
        self.window.wake_overlay_controls()
        self.assertTrue(self.window.video_top_bar.isVisible())
        self.assertTrue(self.window.transport.isVisible())

        # Auto hide
        self.window.video_top_bar.hide()
        self.window.transport.hide()
        self.assertFalse(self.window.video_top_bar.isVisible())
        self.assertFalse(self.window.transport.isVisible())

        # Wake again on mouse movement
        self.window.wake_overlay_controls()
        self.assertTrue(self.window.video_top_bar.isVisible())
        self.assertTrue(self.window.transport.isVisible())

    def test_docked_full_width_video_controls_geometry(self):
        self.window.navigate('Now playing')
        self.app.processEvents()

        w = self.window.width()
        h = self.window.height()
        geo = self.window.transport.geometry()

        # Should be docked at bottom (0px gap), spanning 100% width, height 98px
        self.assertEqual(geo.x(), 0)
        self.assertEqual(geo.width(), w)
        self.assertEqual(geo.y(), h - 98)
        self.assertEqual(geo.height(), 98)

        # Video mode elements active, audio clutter hidden
        self.assertTrue(self.window.video_time_label.isVisible())
        self.assertFalse(self.window.music_track_info.isVisible())
        self.assertFalse(self.window.shuffle.isVisible())
        self.assertFalse(self.window.repeat.isVisible())
        self.assertTrue(self.window.t_sub_btn.isVisible())
        self.assertTrue(self.window.t_snap_btn.isVisible())
        self.assertTrue(self.window.t_bm_btn.isVisible())

        # Exit to library
        self.window.exit_video_to_library()
        self.app.processEvents()

        # Restored audio controls
        self.assertFalse(self.window.video_time_label.isVisible())
        self.assertTrue(self.window.music_track_info.isVisible())
        self.assertTrue(self.window.shuffle.isVisible())
        self.assertTrue(self.window.repeat.isVisible())
        self.assertFalse(self.window.t_sub_btn.isVisible())
        self.assertFalse(self.window.t_snap_btn.isVisible())
        self.assertFalse(self.window.t_bm_btn.isVisible())

    def test_music_now_playing_stage(self):
        # Set current track to Music
        self.window.current = {'path': 'test.mp3', 'title': 'Test Song', 'artist': 'Artist', 'kind': 'Music', 'duration': 180000, 'position': 0}
        self.window.navigate('Now playing')
        self.app.processEvents()

        # Should not enter video watch mode
        self.assertFalse(self.window.is_video_mode)
        self.assertTrue(self.window.music_stage.isVisible())
        self.assertFalse(self.window.video.isVisible())
        self.assertEqual(self.window.music_now_title.text(), 'Test Song')


if __name__ == '__main__':
    unittest.main()

