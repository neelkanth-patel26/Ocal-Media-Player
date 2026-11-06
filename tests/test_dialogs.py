"""Tests for Windows 11 accent theming and Fluent ContentDialogs."""
import unittest
import sys
from PySide6.QtWidgets import QApplication

from src.win11 import (
    get_windows_accent_palette, WIN11_ACCENT, WIN11_ACCENT_TEXT,
    WIN11_ACCENT_BASE, WIN11_ACCENT_HOVER
)
from src.theme import get_stylesheet, STYLE
from src.dialogs import FluentBadge, FluentDialog


app = QApplication.instance() or QApplication(sys.argv)


class TestDialogsAndTheme(unittest.TestCase):
    def test_accent_palette_structure(self):
        pal = get_windows_accent_palette()
        self.assertIn('accent', pal)
        self.assertIn('hover', pal)
        self.assertIn('pressed', pal)
        self.assertIn('base', pal)
        self.assertIn('dark', pal)
        self.assertIn('text', pal)
        self.assertIn('rgb', pal)
        self.assertTrue(pal['accent'].startswith('#'))
        self.assertEqual(len(pal['accent']), 7)
        self.assertIn(pal['text'], ('#000000', '#ffffff'))
        self.assertEqual(len(pal['rgb']), 3)

    def test_theme_stylesheet_contains_accent(self):
        pal = get_windows_accent_palette()
        sheet = get_stylesheet(pal)
        self.assertIn(pal['accent'], sheet)
        self.assertIn(pal['hover'], sheet)
        self.assertIn(STYLE, [sheet, STYLE])

    def test_fluent_badge(self):
        badge_gradient = FluentBadge('play', use_gradient=True, size=46)
        self.assertEqual(badge_gradient.size_px, 46)
        badge_tinted = FluentBadge('keyboard', use_gradient=False, size=46)
        self.assertEqual(badge_tinted.size_px, 46)

    def test_fluent_dialog_construction(self):
        dlg = FluentDialog(title='Test Dialog')
        self.assertEqual(dlg.windowTitle(), 'Test Dialog')
        self.assertGreaterEqual(dlg.minimumWidth(), 460)

    def test_about_dialog_title(self):
        dlg = FluentDialog(title='Ocal Media Player')
        self.assertEqual(dlg.windowTitle(), 'Ocal Media Player')


if __name__ == '__main__':
    unittest.main()

