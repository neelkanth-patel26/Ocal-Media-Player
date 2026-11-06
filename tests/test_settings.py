"""Tests for Ocal Media Player settings, customization, and updater."""
import unittest
import sys
import tempfile
from pathlib import Path
from PySide6.QtWidgets import QApplication

from src.library import Library
from src.win11 import make_accent_palette, get_windows_accent_palette
from src.updater import parse_version, is_newer_version, CURRENT_VERSION
from src.engine import Engine
from src.dialogs import FluentDialog
from src.settings_view import SettingsView


app = QApplication.instance() or QApplication(sys.argv)


class TestSettingsAndCustomization(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.library = Library(directory=Path(self.temp_dir.name))

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_library_settings_defaults(self):
        s = self.library.settings
        self.assertEqual(s.get('theme_mode'), 'system')
        self.assertEqual(s.get('accent_color'), 'system')
        self.assertEqual(s.get('audio_profile'), 'Flat')
        self.assertEqual(s.get('video_aspect'), 'Auto')
        self.assertTrue(s.get('auto_resume'))

    def test_make_accent_palette(self):
        pal = make_accent_palette('#ff6f59', is_light=False)
        self.assertEqual(pal['accent'], '#ff6f59')
        self.assertTrue(pal['hover'].startswith('#'))
        self.assertTrue(pal['pressed'].startswith('#'))
        self.assertIn(pal['text'], ('#000000', '#ffffff'))
        self.assertEqual(pal['rgb'], (255, 111, 89))

        # Test pure white background contrast
        pal_light = make_accent_palette('#ffffff', is_light=True)
        self.assertEqual(pal_light['text'], '#000000')

    def test_version_parsing_and_comparison(self):
        self.assertEqual(parse_version('1.0.0'), (1, 0, 0))
        self.assertEqual(parse_version('v2.1.4'), (2, 1, 4))
        self.assertEqual(parse_version('10.0.17763'), (10, 0, 17763))
        self.assertTrue(is_newer_version('1.0.1', '1.0.0'))
        self.assertTrue(is_newer_version('v2.0.0', '1.9.9'))
        self.assertFalse(is_newer_version('1.0.0', '1.0.0'))
        self.assertFalse(is_newer_version('0.9.9', '1.0.0'))

    def test_engine_equalizer_and_aspect(self):
        engine = Engine()
        try:
            presets = engine.get_equalizer_presets()
            self.assertIn('Flat', presets)
            self.assertIn('Full bass', presets)
            self.assertTrue(engine.set_equalizer_preset('Flat'))
            self.assertTrue(engine.set_equalizer_preset('Full bass'))
            engine.set_aspect_ratio('16:9')
            engine.set_aspect_ratio('Auto')
        finally:
            engine.close()

    def test_settings_view_widgets_and_signals(self):
        view = SettingsView(self.library, engine=None, is_light=False)
        self.assertEqual(view.theme_combo.currentIndex(), 0)  # Follow Windows

        # Test selecting accent
        received_accent = []
        view.accent_color_changed.connect(lambda c: received_accent.append(c))
        view._select_accent_color('#00b4d8')
        self.assertEqual(self.library.settings['accent_color'], '#00b4d8')
        self.assertEqual(received_accent, ['#00b4d8'])

        # Test selecting equalizer profile
        received_eq = []
        view.audio_profile_changed.connect(lambda p: received_eq.append(p))
        idx = view.eq_combo.findData('Full bass')
        view.eq_combo.setCurrentIndex(idx)
        self.assertEqual(self.library.settings['audio_profile'], 'Full bass')
        self.assertEqual(received_eq, ['Full bass'])

        # Test auto_resume toggle
        saved_events = []
        view.setting_saved.connect(lambda k, v: saved_events.append((k, v)))
        view.resume_cb.setChecked(False)
        self.assertFalse(self.library.settings['auto_resume'])
        self.assertIn(('auto_resume', False), saved_events)
        view.resume_cb.setChecked(True)
        self.assertTrue(self.library.settings['auto_resume'])
        self.assertIn(('auto_resume', True), saved_events)

        # Test recently played visibility toggle
        view.show_recent_cb.setChecked(False)
        self.assertFalse(self.library.settings['show_recently_played'])
        self.assertTrue(self.library.settings['hide_recent_view'])
        self.assertIn(('show_recently_played', False), saved_events)
        self.assertIn(('hide_recent_view', True), saved_events)
        view.show_recent_cb.setChecked(True)
        self.assertTrue(self.library.settings['show_recently_played'])
        self.assertFalse(self.library.settings['hide_recent_view'])

        # Test Windows system accent swatch reflects live Windows theme
        win_accent_swatch = None
        for code, btn in view.swatch_buttons:
            if code == 'system':
                win_accent_swatch = btn
                break
        self.assertIsNotNone(win_accent_swatch)
        self.assertTrue(win_accent_swatch.is_system)
        win_pal = get_windows_accent_palette(view.is_light)
        self.assertEqual(win_accent_swatch.system_accent, win_pal['accent'])
        self.assertIn(win_pal['accent'], win_accent_swatch.toolTip())

    def test_player_window_respects_navigation_and_resume_settings(self):
        from src.app import PlayerWindow
        window = PlayerWindow(self.library)
        try:
            # Initially visible (not hidden)
            self.assertFalse(window.nav['Recently played'].isHidden())

            # Disable recently played
            window.settings_view.show_recent_cb.setChecked(False)
            self.assertTrue(window.nav['Recently played'].isHidden())

            # Attempt to navigate to Recently played should route to All media
            window.navigate('Recently played')
            self.assertEqual(window.view, 'All media')

            # Re-enable
            window.settings_view.show_recent_cb.setChecked(True)
            self.assertFalse(window.nav['Recently played'].isHidden())
        finally:
            window.close()


if __name__ == '__main__':
    unittest.main()
