"""Native Windows 11 DWM and Fluent Design integration for GNS Player."""
import ctypes
import os
import sys
from ctypes import c_int, byref, sizeof
from PySide6.QtGui import QFont, QFontDatabase, QGuiApplication

# Windows 11 DWM attribute IDs
DWMWA_USE_IMMERSIVE_DARK_MODE = 20
DWMWA_WINDOW_CORNER_PREFERENCE = 33
DWMWA_BORDER_COLOR = 34
DWMWA_CAPTION_COLOR = 35
DWMWA_TEXT_COLOR = 36
DWMWA_SYSTEMBACKDROP_TYPE = 38

# DWM constants
DWMWCP_DEFAULT = 0
DWMWCP_DONOTROUND = 1      # Windows 11 square window corners
DWMWCP_ROUND = 2           # Windows 11 rounded window corners
DWMWCP_ROUNDSMALL = 3
DWMSBT_MAINWINDOW = 2      # Windows 11 Mica material backdrop
DWMSBT_TRANSIENTWINDOW = 3 # Windows 11 Acrylic material backdrop
DWMSBT_TABBEDWINDOW = 4    # Windows 11 Tabbed Mica backdrop


def is_windows_light_theme() -> bool:
    """Check if Windows 10/11 is set to Light theme for applications."""
    if sys.platform == 'win32':
        try:
            import winreg
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r'Software\Microsoft\Windows\CurrentVersion\Themes\Personalize'
            ) as key:
                val, _ = winreg.QueryValueEx(key, 'AppsUseLightTheme')
                return bool(val)
        except Exception:
            pass
    try:
        app = QGuiApplication.instance()
        if app is not None:
            bg = app.palette().window().color()
            if bg.isValid():
                return bg.lightness() > 128
    except Exception:
        pass
    return False


def make_accent_palette(hex_str: str, is_light: bool):
    """Generate an accent palette dict from an arbitrary hex color code."""
    hex_str = hex_str.strip()
    if not hex_str.startswith('#'):
        hex_str = '#' + hex_str
    if len(hex_str) != 7:
        hex_str = '#0078d4' if is_light else '#60cdff'
    try:
        r = int(hex_str[1:3], 16)
        g = int(hex_str[3:5], 16)
        b = int(hex_str[5:7], 16)
    except Exception:
        r, g, b = (0, 120, 212) if is_light else (96, 205, 255)
        hex_str = f'#{r:02x}{g:02x}{b:02x}'
    lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255.0
    hover_r = min(255, int(r * 1.15))
    hover_g = min(255, int(g * 1.15))
    hover_b = min(255, int(b * 1.15))
    press_r = max(0, int(r * 0.85))
    press_g = max(0, int(g * 0.85))
    press_b = max(0, int(b * 0.85))
    return {
        'accent': hex_str,
        'hover': f'#{hover_r:02x}{hover_g:02x}{hover_b:02x}',
        'pressed': f'#{press_r:02x}{press_g:02x}{press_b:02x}',
        'base': hex_str,
        'dark': f'#{press_r:02x}{press_g:02x}{press_b:02x}',
        'text': '#000000' if lum > 0.55 else '#ffffff',
        'rgb': (r, g, b)
    }


def get_windows_accent_palette(is_light=None, custom_accent_hex=None):
    """
    Query Windows 11 system accent palette from registry or custom hex override.
    Returns a dict with:
      'accent': primary accent for dark/light theme (e.g. '#ea9a81' dark, '#ce4937' light)
      'hover': lighter hover state
      'pressed': pressed state
      'base': base Windows accent
      'dark': dark accent
      'text': high-contrast text color ('#000000' or '#ffffff')
      'rgb': (r, g, b) tuple of integers
    """
    if is_light is None:
        is_light = is_windows_light_theme()

    if custom_accent_hex and custom_accent_hex.lower() != 'system':
        return make_accent_palette(custom_accent_hex, is_light)

    if sys.platform == 'win32':
        try:
            import winreg
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r'Software\Microsoft\Windows\CurrentVersion\Explorer\Accent'
            ) as key:
                val, _ = winreg.QueryValueEx(key, 'AccentPalette')
                if val and len(val) >= 28:
                    colors = [f'#{val[i]:02x}{val[i+1]:02x}{val[i+2]:02x}' for i in range(0, len(val), 4)]
                    if is_light:
                        # Windows 11 uses base accent (palette[3]) for readable contrast on light backgrounds
                        r, g, b = val[12], val[13], val[14]
                        lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255.0
                        return {
                            'accent': colors[3],
                            'hover': colors[2],
                            'pressed': colors[4],
                            'base': colors[3],
                            'dark': colors[5],
                            'text': '#000000' if lum > 0.55 else '#ffffff',
                            'rgb': (r, g, b)
                        }
                    else:
                        # palette[1] is the primary light accent used on Windows 11 dark theme
                        r, g, b = val[4], val[5], val[6]
                        lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255.0
                        return {
                            'accent': colors[1],
                            'hover': colors[0],
                            'pressed': colors[2],
                            'base': colors[3],
                            'dark': colors[4],
                            'text': '#000000' if lum > 0.55 else '#ffffff',
                            'rgb': (r, g, b)
                        }
        except Exception:
            pass

    # Secondary fallback: QGuiApplication palette accent if Qt is running
    try:
        app = QGuiApplication.instance()
        if app is not None:
            c = app.palette().accent().color()
            if c.isValid():
                hex_name = c.name()
                r, g, b = c.red(), c.green(), c.blue()
                lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255.0
                hover_r = min(255, int(r * 1.15))
                hover_g = min(255, int(g * 1.15))
                hover_b = min(255, int(b * 1.15))
                press_r = max(0, int(r * 0.85))
                press_g = max(0, int(g * 0.85))
                press_b = max(0, int(b * 0.85))
                return {
                    'accent': hex_name,
                    'hover': f'#{hover_r:02x}{hover_g:02x}{hover_b:02x}',
                    'pressed': f'#{press_r:02x}{press_g:02x}{press_b:02x}',
                    'base': hex_name,
                    'dark': f'#{press_r:02x}{press_g:02x}{press_b:02x}',
                    'text': '#000000' if lum > 0.55 else '#ffffff',
                    'rgb': (r, g, b)
                }
    except Exception:
        pass

    # Default fallback: Windows 11 default Cyan (Dark) or Blue (Light)
    if is_light:
        return {
            'accent': '#0078d4',
            'hover': '#106ebe',
            'pressed': '#005a9e',
            'base': '#0078d4',
            'dark': '#004578',
            'text': '#ffffff',
            'rgb': (0, 120, 212)
        }
    return {
        'accent': '#60cdff',
        'hover': '#78d5ff',
        'pressed': '#49b3e8',
        'base': '#0078d4',
        'dark': '#005a9e',
        'text': '#000000',
        'rgb': (96, 205, 255)
    }


def rgba(palette, alpha):
    """Format an rgba() string from a palette dict and alpha float."""
    r, g, b = palette.get('rgb', (96, 205, 255))
    return f'rgba({r}, {g}, {b}, {alpha})'


def refresh_win11_theme(custom_accent_hex=None):
    """Reload active Windows 11 theme mode and accent palette."""
    global ACCENT_PALETTE, WIN11_ACCENT, WIN11_ACCENT_HOVER, WIN11_ACCENT_PRESSED
    global WIN11_ACCENT_BASE, WIN11_ACCENT_DARK, WIN11_ACCENT_TEXT, WIN11_ACCENT_RGB
    global WIN11_BG, WIN11_SIDEBAR, WIN11_CARD, WIN11_TRANSPORT, WIN11_TEXT_PRIMARY, WIN11_TEXT_MUTED, WIN11_BORDER
    is_light = is_windows_light_theme()
    if custom_accent_hex and custom_accent_hex.lower() != 'system':
        ACCENT_PALETTE = make_accent_palette(custom_accent_hex, is_light)
    else:
        ACCENT_PALETTE = get_windows_accent_palette(is_light)
    WIN11_ACCENT = ACCENT_PALETTE['accent']
    WIN11_ACCENT_HOVER = ACCENT_PALETTE['hover']
    WIN11_ACCENT_PRESSED = ACCENT_PALETTE['pressed']
    WIN11_ACCENT_BASE = ACCENT_PALETTE['base']
    WIN11_ACCENT_DARK = ACCENT_PALETTE['dark']
    WIN11_ACCENT_TEXT = ACCENT_PALETTE['text']
    WIN11_ACCENT_RGB = ACCENT_PALETTE['rgb']

    if is_light:
        WIN11_BG = '#f3f3f3'
        WIN11_SIDEBAR = '#f3f3f3'
        WIN11_CARD = '#ffffff'
        WIN11_TRANSPORT = '#ffffff'
        WIN11_TEXT_PRIMARY = '#1b1b1b'
        WIN11_TEXT_MUTED = '#616161'
        WIN11_BORDER = 'rgba(0, 0, 0, 0.08)'
    else:
        WIN11_BG = '#202020'
        WIN11_SIDEBAR = '#181818'
        WIN11_CARD = '#272727'
        WIN11_TRANSPORT = '#212121'
        WIN11_TEXT_PRIMARY = '#f3f3f3'
        WIN11_TEXT_MUTED = '#9d9d9d'
        WIN11_BORDER = 'rgba(255, 255, 255, 0.08)'
    return is_light, ACCENT_PALETTE


# Dynamically initialize Windows 11 Fluent Palette to match user's OS color theme
ACCENT_PALETTE = get_windows_accent_palette()
WIN11_ACCENT = ACCENT_PALETTE['accent']
WIN11_ACCENT_HOVER = ACCENT_PALETTE['hover']
WIN11_ACCENT_PRESSED = ACCENT_PALETTE['pressed']
WIN11_ACCENT_BASE = ACCENT_PALETTE['base']
WIN11_ACCENT_DARK = ACCENT_PALETTE['dark']
WIN11_ACCENT_TEXT = ACCENT_PALETTE['text']
WIN11_ACCENT_RGB = ACCENT_PALETTE['rgb']

if is_windows_light_theme():
    WIN11_BG = '#f3f3f3'
    WIN11_SIDEBAR = '#f3f3f3'
    WIN11_CARD = '#ffffff'
    WIN11_TRANSPORT = '#ffffff'
    WIN11_TEXT_PRIMARY = '#1b1b1b'
    WIN11_TEXT_MUTED = '#616161'
    WIN11_BORDER = 'rgba(0, 0, 0, 0.08)'
else:
    WIN11_BG = '#202020'
    WIN11_SIDEBAR = '#181818'
    WIN11_CARD = '#272727'
    WIN11_TRANSPORT = '#212121'
    WIN11_TEXT_PRIMARY = '#f3f3f3'
    WIN11_TEXT_MUTED = '#9d9d9d'
    WIN11_BORDER = 'rgba(255, 255, 255, 0.08)'

# Windows 11 Segoe Fluent Icons glyph mapping
GLYPHS = {
    'home': '\uE80F',            # Home
    'music': '\uE8D6',           # MusicNote / MusicInfo
    'video': '\uE8B2',           # Video
    'queue': '\uE90B',           # PlayList / Queue
    'heart_fill': '\uEB52',      # Heart filled
    'heart_outline': '\uEB51',   # Heart outline
    'history': '\uE81C',         # History / Recently played
    'play': '\uE768',            # Play
    'pause': '\uE769',           # Pause
    'prev': '\uE892',            # Previous
    'next': '\uE893',            # Next
    'back10': '\uE7A1',          # Rotate counter-clockwise / step back
    'fwd10': '\uE7A2',           # Rotate clockwise / step forward
    'shuffle': '\uE8B1',         # Shuffle
    'repeat': '\uE8EE',          # RepeatAll
    'volume': '\uE767',          # Volume
    'mute': '\uE74F',            # Mute
    'fullscreen': '\uE740',      # FullScreen
    'restore': '\uE73F',         # BackToWindow
    'search': '\uE721',          # Search
    'open_file': '\uE8E5',       # FolderOpen / Open file
    'folder': '\uED25',          # FolderHorizontal / Add folder
    'stream': '\uE774',          # Globe / Network stream
    'info': '\uE946',            # Info / About
    'keyboard': '\uE765',        # Keyboard / Shortcuts
    'subtitles': '\uED1E',       # ClosedCaption / Subtitles
    'camera': '\uE722',          # Camera / Snapshot
    'pin': '\uE718',             # Pin / Always on top
    'clock': '\uE823',           # Clock / Sleep timer
    'more': '\uE712',            # More options
    'bookmark': '\uE734',        # FavoriteStar / Bookmark
    'speed': '\uEC57',           # PlaybackRate / Speed
}

_HAS_FLUENT_ICONS = False


def init_win11_fonts():
    """Detect presence of native Windows 11 Segoe Fluent Icons."""
    global _HAS_FLUENT_ICONS
    try:
        families = QFontDatabase.families()
        _HAS_FLUENT_ICONS = 'Segoe Fluent Icons' in families or 'Segoe MDL2 Assets' in families
    except Exception:
        _HAS_FLUENT_ICONS = False


def glyph(name, fallback=''):
    """Return the Segoe Fluent Icon glyph or clean Unicode fallback."""
    if _HAS_FLUENT_ICONS and name in GLYPHS:
        return GLYPHS[name]
    fallbacks = {
        'home': '⌂', 'music': '♪', 'video': '▶', 'queue': '☰',
        'heart_fill': '♥', 'heart_outline': '♡', 'history': '◷',
        'play': '▶', 'pause': '⏸', 'prev': '⏮', 'next': '⏭',
        'back10': '⟲ 10', 'fwd10': '⟳ 10', 'shuffle': '🔀', 'repeat': '🔁',
        'volume': '🔊', 'mute': '🔇', 'fullscreen': '⛶', 'restore': '🗗',
        'search': '🔍', 'open_file': '📂', 'folder': '📁', 'stream': '🌐',
        'info': 'ℹ', 'keyboard': '⌨', 'subtitles': 'CC', 'camera': '📷',
        'pin': '📌', 'clock': '⏱', 'more': '⋯', 'bookmark': '★', 'speed': '⚡'
    }
    return fallbacks.get(name, fallback or GLYPHS.get(name, ''))


def apply_win11_attributes(window, is_light=None, caption_color_hex=None):
    """
    Apply native Windows 11 DWM attributes to the window handle:
    - Immersive dark/light mode on the native title bar (DWMWA_USE_IMMERSIVE_DARK_MODE)
    - Windows 11 rounded window corners (DWMWA_WINDOW_CORNER_PREFERENCE)
    - Windows 11 Mica backdrop material (DWMWA_SYSTEMBACKDROP_TYPE)
    - Matching caption and text colors
    """
    if sys.platform != 'win32':
        return False
    if is_light is None:
        is_light = is_windows_light_theme()
    try:
        hwnd = int(window.winId())
        dwm = ctypes.windll.dwmapi

        # 0 for light mode, 1 for immersive dark mode
        dark = c_int(0 if is_light else 1)
        dwm.DwmSetWindowAttribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, byref(dark), sizeof(dark))

        # Request Windows 11 rounded window corners
        corners = c_int(DWMWCP_ROUND)
        dwm.DwmSetWindowAttribute(hwnd, DWMWA_WINDOW_CORNER_PREFERENCE, byref(corners), sizeof(corners))

        # Enable Windows 11 Mica backdrop effect
        backdrop = c_int(DWMSBT_MAINWINDOW)
        dwm.DwmSetWindowAttribute(hwnd, DWMWA_SYSTEMBACKDROP_TYPE, byref(backdrop), sizeof(backdrop))

        # Match caption / titlebar background color
        if caption_color_hex is None:
            # 0x00F3F3F3 for light, 0x00202020 for dark (COLORREF BGR)
            caption_color_hex = 0x00F3F3F3 if is_light else 0x00202020
        caption_color = c_int(caption_color_hex)
        dwm.DwmSetWindowAttribute(hwnd, DWMWA_CAPTION_COLOR, byref(caption_color), sizeof(caption_color))

        # Titlebar text color
        text_color = c_int(0x00000000 if is_light else 0x00FFFFFF)
        dwm.DwmSetWindowAttribute(hwnd, DWMWA_TEXT_COLOR, byref(text_color), sizeof(text_color))

        # Border color
        border_color = c_int(0x00E0E0E0 if is_light else 0x00333333)
        dwm.DwmSetWindowAttribute(hwnd, DWMWA_BORDER_COLOR, byref(border_color), sizeof(border_color))

        return True
    except Exception:
        return False


class DWM_MARGINS(ctypes.Structure):
    _fields_ = [
        ('cxLeftWidth', c_int),
        ('cxRightWidth', c_int),
        ('cyTopHeight', c_int),
        ('cyBottomHeight', c_int)
    ]


def apply_win11_frameless_attributes(window, is_light=None):
    """
    Apply native Windows 11 DWM attributes to a frameless extended window:
    - Immersive dark/light mode (DWMWA_USE_IMMERSIVE_DARK_MODE)
    - Windows 11 rounded window corners when restored, square when maximized/fullscreen
    - Ensures 100% solid, opaque client area with zero desktop bleed-through
    """
    if sys.platform != 'win32':
        return False
    if is_light is None:
        is_light = is_windows_light_theme()
    try:
        hwnd = int(window.winId())
        dwm = ctypes.windll.dwmapi

        # 0 for light mode, 1 for dark mode
        dark = c_int(0 if is_light else 1)
        dwm.DwmSetWindowAttribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, byref(dark), sizeof(dark))

        # Check if window is currently maximized or fullscreen
        is_max = False
        try:
            is_max = window.isMaximized() or window.isFullScreen()
        except Exception:
            pass

        # Windows 11 rounded window corners: DO NOT round when maximized or fullscreen
        corner_val = DWMWCP_DONOTROUND if is_max else DWMWCP_ROUND
        corners = c_int(corner_val)
        dwm.DwmSetWindowAttribute(hwnd, DWMWA_WINDOW_CORNER_PREFERENCE, byref(corners), sizeof(corners))

        # Do not extend frame glass margins into client area (prevents see-through desktop bleed)
        margins = DWM_MARGINS(0, 0, 0, 0)
        dwm.DwmExtendFrameIntoClientArea(hwnd, byref(margins))

        return True
    except Exception:
        return False

