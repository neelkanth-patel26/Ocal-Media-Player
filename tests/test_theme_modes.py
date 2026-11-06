"""Unit tests for Light Mode, Dark Mode, and live dynamic theme updates."""
import unittest
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QColor

from src.win11 import (
    is_windows_light_theme, get_windows_accent_palette,
    refresh_win11_theme, apply_win11_attributes, apply_win11_frameless_attributes
)
from src.theme import get_stylesheet
from src.artwork import create_fallback_artwork, get_media_artwork, clear_artwork_cache
from src.app import PlayerWindow, MediaThumbnail
from src.library import Library


app = QApplication.instance() or QApplication([])


class TestThemeModes(unittest.TestCase):
    def test_accent_palette_modes(self):
        pal_dark = get_windows_accent_palette(is_light=False)
        pal_light = get_windows_accent_palette(is_light=True)

        self.assertIn('accent', pal_dark)
        self.assertIn('hover', pal_dark)
        self.assertIn('pressed', pal_dark)
        self.assertIn('text', pal_dark)
        self.assertIn('rgb', pal_dark)

        self.assertIn('accent', pal_light)
        self.assertIn('hover', pal_light)
        self.assertIn('pressed', pal_light)
        self.assertIn('text', pal_light)
        self.assertIn('rgb', pal_light)

        # Confirm colors are valid hex colors
        self.assertTrue(QColor(pal_dark['accent']).isValid())
        self.assertTrue(QColor(pal_light['accent']).isValid())
        self.assertIn(pal_dark['text'], ('#000000', '#ffffff'))
        self.assertIn(pal_light['text'], ('#000000', '#ffffff'))

    def test_stylesheet_generation_both_modes(self):
        style_dark = get_stylesheet(is_light=False)
        style_light = get_stylesheet(is_light=True)

        self.assertIn('background: #202020', style_dark)
        self.assertIn('background: #181818', style_dark)
        self.assertIn('color: #f3f3f3', style_dark)

        self.assertIn('background: #f3f3f3', style_light)
        self.assertIn('background: #ffffff', style_light)
        self.assertIn('color: #1b1b1b', style_light)

    def test_fallback_artwork_modes(self):
        dark_art = create_fallback_artwork('Music', 140, 8, is_light=False)
        light_art = create_fallback_artwork('Music', 140, 8, is_light=True)

        self.assertFalse(dark_art.isNull())
        self.assertFalse(light_art.isNull())
        self.assertEqual(dark_art.size(), light_art.size())

    def test_media_thumbnail_theme_awareness(self):
        thumb = MediaThumbnail(is_light=False, accent='#ea9a81')
        self.assertFalse(thumb.is_light)
        self.assertEqual(thumb.accent, '#ea9a81')

        thumb.set_theme(is_light=True, accent='#ce4937')
        self.assertTrue(thumb.is_light)
        self.assertEqual(thumb.accent, '#ce4937')

    def test_player_window_live_theme_switching(self):
        lib = Library()
        win = PlayerWindow(lib)

        # Initial state
        initial_mode = win.is_light

        # Simulate dynamic switch to light mode
        win.is_light = True
        win.palette = get_windows_accent_palette(is_light=True)
        win.update_theme_elements()
        self.assertEqual(win.media_thumb.is_light, True)
        self.assertEqual(win.media_thumb.accent, win.palette['accent'])

        # Simulate dynamic switch to dark mode
        win.is_light = False
        win.palette = get_windows_accent_palette(is_light=False)
        win.update_theme_elements()
        self.assertEqual(win.media_thumb.is_light, False)
        self.assertEqual(win.media_thumb.accent, win.palette['accent'])

        # Test check_system_theme runs cleanly
        win.check_system_theme(force=True)

        win.close()


if __name__ == '__main__':
    unittest.main()

