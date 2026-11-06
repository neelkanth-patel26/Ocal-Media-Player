"""Windows 11 Fluent Settings View for Ocal Media Player."""
import os
import subprocess
from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QComboBox, QCheckBox, QLineEdit, QScrollArea,
    QProgressBar, QSizePolicy
)
from PySide6.QtCore import Qt, Signal, QRectF, QPropertyAnimation, Property, QEasingCurve, QSize
from PySide6.QtGui import QColor, QPainter, QBrush, QPen, QFont

from .icons import get_icon
from .win11 import get_windows_accent_palette, is_windows_light_theme, make_accent_palette
from .updater import UpdateCheckerThread, UpdateDownloaderThread, launch_installer_and_exit, CURRENT_VERSION
from .system_integration import is_registered_in_default_apps, register_default_media_player, open_windows_default_apps_settings


class ColorSwatchButton(QPushButton):
    """Clickable color swatch with rounded corners, selection ring, and Windows logo."""
    def __init__(self, color_hex, name, selected=False, is_system=False, system_accent='#0078d4', system_text='#ffffff', parent=None):
        super().__init__(parent)
        self.color_hex = color_hex
        self.swatch_name = name
        self.is_selected = selected
        self.is_system = is_system
        self.system_accent = system_accent
        self.system_text = system_text
        self.setFixedSize(32, 32)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._update_tooltip()

    def _update_tooltip(self):
        if self.is_system:
            self.setToolTip(f"{self.swatch_name} ({self.system_accent})")
        else:
            self.setToolTip(f"{self.swatch_name} ({self.color_hex})")

    def update_system_color(self, accent_hex, text_hex):
        """Update live system color and refresh swatch."""
        self.system_accent = accent_hex
        self.system_text = text_hex
        self._update_tooltip()
        self.update()

    def setSelected(self, sel):
        self.is_selected = sel
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()

        if self.is_system:
            # Live Windows system theme accent color
            bg_color = QColor(self.system_accent)
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(bg_color)
            p.drawRoundedRect(QRectF(3, 3, w - 6, h - 6), 7, 7)

            # Windows 11 4-tile logo centered
            tile_sz = 4.2
            gap = 1.6
            total_sz = tile_sz * 2 + gap
            cx = (w - total_sz) / 2.0
            cy = (h - total_sz) / 2.0

            logo_color = QColor(self.system_text if self.system_text else '#ffffff')
            p.setBrush(logo_color)
            p.drawRect(QRectF(cx, cy, tile_sz, tile_sz))
            p.drawRect(QRectF(cx + tile_sz + gap, cy, tile_sz, tile_sz))
            p.drawRect(QRectF(cx, cy + tile_sz + gap, tile_sz, tile_sz))
            p.drawRect(QRectF(cx + tile_sz + gap, cy + tile_sz + gap, tile_sz, tile_sz))
        else:
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(QColor(self.color_hex))
            p.drawRoundedRect(QRectF(3, 3, w - 6, h - 6), 7, 7)

        if self.is_selected:
            # High-contrast selection ring
            ring_col = QColor('#ffffff')
            pen = QPen(ring_col, 2)
            p.setPen(pen)
            p.setBrush(Qt.BrushStyle.NoBrush)
            p.drawRoundedRect(QRectF(1, 1, w - 2, h - 2), 9, 9)
        p.end()


class FluentToggleSwitch(QCheckBox):
    """Windows 11 Fluent Design animated toggle switch with 'On'/'Off' indicator."""
    def __init__(self, parent=None, is_light=False, accent='#ff6f59', accent_text='#ffffff'):
        super().__init__(parent)
        self.is_light = is_light
        self.accent = accent
        self.accent_text = accent_text
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._thumb_pos = 1.0 if self.isChecked() else 0.0
        self.setFixedSize(76, 24)

        self._anim = QPropertyAnimation(self, b'thumb_pos', self)
        self._anim.setDuration(160)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.toggled.connect(self._on_toggled)

    def _get_thumb_pos(self):
        return self._thumb_pos

    def _set_thumb_pos(self, val):
        self._thumb_pos = val
        self.update()

    thumb_pos = Property(float, _get_thumb_pos, _set_thumb_pos)

    def _on_toggled(self, checked):
        self._anim.stop()
        self._anim.setStartValue(self._thumb_pos)
        self._anim.setEndValue(1.0 if checked else 0.0)
        self._anim.start()

    def setChecked(self, checked):
        prev = self.isChecked()
        super().setChecked(checked)
        if prev != checked:
            self._thumb_pos = 1.0 if checked else 0.0
            self.update()

    def apply_theme(self, is_light, accent, accent_text):
        self.is_light = is_light
        self.accent = accent
        self.accent_text = accent_text
        self.update()

    def sizeHint(self):
        return QSize(76, 24)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setRenderHint(QPainter.RenderHint.TextAntialiasing)

        checked = self.isChecked()
        pos = self._thumb_pos

        sw_w = 40.0
        sw_h = 20.0
        sw_x = 0.0
        sw_y = (self.height() - sw_h) / 2.0
        r = sw_h / 2.0

        if self.is_light:
            off_border = QColor(0, 0, 0, 110)
            off_bg = QColor(0, 0, 0, 10)
            off_thumb = QColor('#5d5d5d')
            text_color = QColor('#1b1b1b')
        else:
            off_border = QColor(255, 255, 255, 120)
            off_bg = QColor(255, 255, 255, 15)
            off_thumb = QColor('#cecece')
            text_color = QColor('#ffffff')

        accent_col = QColor(self.accent)
        accent_txt = QColor(self.accent_text)

        if pos > 0.01:
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(accent_col)
            p.drawRoundedRect(QRectF(sw_x, sw_y, sw_w, sw_h), r, r)
        else:
            p.setPen(QPen(off_border, 1.2))
            p.setBrush(off_bg)
            p.drawRoundedRect(QRectF(sw_x + 0.6, sw_y + 0.6, sw_w - 1.2, sw_h - 1.2), r, r)

        thumb_diam = 12.0
        start_x = sw_x + 4.0
        end_x = sw_x + sw_w - thumb_diam - 4.0
        thumb_x = start_x + (end_x - start_x) * pos
        thumb_y = sw_y + (sw_h - thumb_diam) / 2.0

        thumb_color = accent_txt if pos > 0.5 else off_thumb
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(thumb_color)
        p.drawEllipse(QRectF(thumb_x, thumb_y, thumb_diam, thumb_diam))

        f = QFont('Segoe UI Variable Display', 9, QFont.Weight.Medium)
        f.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
        p.setFont(f)
        p.setPen(text_color)
        text_str = 'On' if checked else 'Off'
        p.drawText(QRectF(sw_w + 8, 0, self.width() - sw_w - 8, self.height()),
                   Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, text_str)
        p.end()


class SettingCard(QFrame):
    """Windows 11 Fluent settings card with subtle border and rounded styling."""
    def __init__(self, is_light=False, parent=None):
        super().__init__(parent)
        self.is_light = is_light
        self.setObjectName('settingCard')
        self.update_style(is_light)

    def update_style(self, is_light):
        self.is_light = is_light
        if is_light:
            bg = '#ffffff'
            border = '1px solid rgba(0, 0, 0, 0.08)'
        else:
            bg = 'rgba(255, 255, 255, 0.04)'
            border = '1px solid rgba(255, 255, 255, 0.07)'
        self.setStyleSheet(f"""
            QFrame#settingCard {{
                background: {bg};
                border: {border};
                border-radius: 8px;
            }}
        """)


class SettingsView(QWidget):
    """Complete Fluent Design Settings View for Ocal Media Player."""
    # Signals for live application updates
    theme_mode_changed = Signal(str)         # 'system', 'dark', 'light'
    accent_color_changed = Signal(str)       # 'system' or hex string
    audio_profile_changed = Signal(str)      # Equalizer preset name
    video_aspect_changed = Signal(str)       # Aspect ratio string
    setting_saved = Signal(str, object)      # (key, value)

    PRESET_COLORS = [
        ('system', 'Windows Accent', True),
        ('#ff6f59', 'Coral Red (Ocal Default)', False),
        ('#00b4d8', 'Sky Cyan', False),
        ('#10b981', 'Emerald Green', False),
        ('#8b5cf6', 'Amethyst Purple', False),
        ('#f59e0b', 'Amber Gold', False),
        ('#f97316', 'Sunset Orange', False),
        ('#6366f1', 'Electric Indigo', False),
        ('#ec4899', 'Rose Pink', False),
    ]

    EQUALIZER_PRESETS = [
        ('Flat', 'Flat (Standard / Uncolored)'),
        ('Full bass', 'Full Bass (Bass Boost)'),
        ('Full bass and treble', 'Full Bass & Treble (V-Curve)'),
        ('Headphones', 'Headphones (Spatial Acoustic)'),
        ('Rock', 'Rock & Metal'),
        ('Pop', 'Pop & Vocal Clarity'),
        ('Classical', 'Classical & Orchestral'),
        ('Techno', 'Techno & Electronic'),
        ('Dance', 'Dance & Club Beat'),
        ('Live', 'Live Concert & Immersion'),
        ('Party', 'Party & Punchy Highs'),
        ('Soft', 'Soft & Ambient Background'),
        ('Full treble', 'Full Treble (Bright Highs)'),
    ]

    ASPECT_RATIOS = [
        ('Auto', 'Auto (Default / Original Aspect)'),
        ('16:9', '16:9 (Standard Widescreen)'),
        ('4:3', '4:3 (Traditional TV / CRT)'),
        ('21:9', '21:9 (Cinematic Ultrawide)'),
        ('16:10', '16:10 (Computer Display Fill)'),
    ]

    def __init__(self, library, engine, parent=None, is_light=False):
        super().__init__(parent)
        self.library = library
        self.engine = engine
        self.is_light = is_light
        self.palette_data = get_windows_accent_palette(is_light)
        self.swatch_buttons = []
        self.checker_thread = None
        self.downloader_thread = None
        self.downloaded_installer_path = None

        self._build_ui()
        self.load_settings()

    def _build_ui(self):
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # Scroll Area for fluent settings
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setStyleSheet("QScrollArea { background: transparent; border: none; }")

        container = QWidget()
        container.setStyleSheet("background: transparent;")
        self.c_layout = QVBoxLayout(container)
        self.c_layout.setContentsMargins(10, 0, 20, 24)
        self.c_layout.setSpacing(16)

        # Header
        header_box = QVBoxLayout()
        header_box.setSpacing(4)
        self.title_lbl = QLabel('Settings')
        self.title_lbl.setStyleSheet('font-size: 26px; font-weight: 700; letter-spacing: -0.5px;')
        header_box.addWidget(self.title_lbl)

        self.subtitle_lbl = QLabel('Personalize appearance, sound profile, video display, and updates')
        self.subtitle_lbl.setObjectName('dialogMuted')
        self.subtitle_lbl.setStyleSheet('font-size: 13px; color: #888888;')
        header_box.addWidget(self.subtitle_lbl)
        self.c_layout.addLayout(header_box)
        self.c_layout.addSpacing(6)

        # -------------------------------------------------------------
        # Section 1: Appearance & Personalization
        # -------------------------------------------------------------
        self.c_layout.addWidget(self._create_section_label('APPEARANCE & PERSONALIZATION'))

        # Theme Mode Card
        theme_card = SettingCard(self.is_light)
        t_layout = QVBoxLayout(theme_card)
        t_layout.setContentsMargins(16, 14, 16, 14)
        t_layout.setSpacing(8)

        t_row = QHBoxLayout()
        t_texts = QVBoxLayout()
        t_texts.setSpacing(2)
        t_title = QLabel('App Theme')
        t_title.setStyleSheet('font-size: 14px; font-weight: 600;')
        t_desc = QLabel('Select which theme to display for Ocal Media Player')
        t_desc.setStyleSheet('font-size: 12px; color: #888888;')
        t_texts.addWidget(t_title)
        t_texts.addWidget(t_desc)
        t_row.addLayout(t_texts, 1)

        self.theme_combo = QComboBox()
        self.theme_combo.setMinimumWidth(180)
        self.theme_combo.addItems(['Follow Windows (Auto)', 'Dark Mode', 'Light Mode'])
        self.theme_combo.currentIndexChanged.connect(self._on_theme_combo_changed)
        t_row.addWidget(self.theme_combo)
        t_layout.addLayout(t_row)
        self.c_layout.addWidget(theme_card)

        # Accent Color Card
        accent_card = SettingCard(self.is_light)
        a_layout = QVBoxLayout(accent_card)
        a_layout.setContentsMargins(16, 14, 16, 14)
        a_layout.setSpacing(10)

        a_row = QHBoxLayout()
        a_texts = QVBoxLayout()
        a_texts.setSpacing(2)
        a_title = QLabel('Accent Color')
        a_title.setStyleSheet('font-size: 14px; font-weight: 600;')
        a_desc = QLabel('Choose a custom accent color or follow the Windows system accent')
        a_desc.setStyleSheet('font-size: 12px; color: #888888;')
        a_texts.addWidget(a_title)
        a_texts.addWidget(a_desc)
        a_row.addLayout(a_texts, 1)
        a_layout.addLayout(a_row)

        # Color Swatches Row
        swatch_row = QHBoxLayout()
        swatch_row.setSpacing(10)
        win_pal = get_windows_accent_palette(self.is_light)
        for hex_code, name, is_sys in self.PRESET_COLORS:
            btn = ColorSwatchButton(
                hex_code, name,
                is_system=is_sys,
                system_accent=win_pal['accent'],
                system_text=win_pal.get('text', '#ffffff')
            )
            btn.clicked.connect(lambda ch=False, c=hex_code: self._select_accent_color(c))
            swatch_row.addWidget(btn)
            self.swatch_buttons.append((hex_code, btn))

        swatch_row.addSpacing(12)
        # Custom hex input
        self.hex_input = QLineEdit()
        self.hex_input.setPlaceholderText('#ff6f59')
        self.hex_input.setMaxLength(7)
        self.hex_input.setFixedWidth(86)
        swatch_row.addWidget(self.hex_input)

        self.hex_apply_btn = QPushButton('Apply')
        self.hex_apply_btn.setFixedWidth(64)
        self.hex_apply_btn.clicked.connect(self._apply_custom_hex)
        swatch_row.addWidget(self.hex_apply_btn)

        swatch_row.addStretch(1)
        a_layout.addLayout(swatch_row)
        self.c_layout.addWidget(accent_card)

        # Navigation / Sidebar Card
        nav_card = SettingCard(self.is_light)
        n_layout = QVBoxLayout(nav_card)
        n_layout.setContentsMargins(16, 14, 16, 14)
        n_layout.setSpacing(10)

        n_row = QHBoxLayout()
        n_texts = QVBoxLayout()
        n_texts.setSpacing(2)
        n_title = QLabel('Recently Played View')
        n_title.setStyleSheet('font-size: 14px; font-weight: 600;')
        n_desc = QLabel('Show or hide the Recently played tab in the left sidebar navigation')
        n_desc.setStyleSheet('font-size: 12px; color: #888888;')
        n_texts.addWidget(n_title)
        n_texts.addWidget(n_desc)
        n_row.addLayout(n_texts, 1)

        accent = self.palette_data.get('accent', '#ff6f59')
        accent_text = self.palette_data.get('text', '#ffffff')

        self.show_recent_cb = FluentToggleSwitch(self, is_light=self.is_light, accent=accent, accent_text=accent_text)
        self.show_recent_cb.toggled.connect(self._on_recent_view_toggled)
        n_row.addWidget(self.show_recent_cb)
        n_layout.addLayout(n_row)
        self.c_layout.addWidget(nav_card)

        # -------------------------------------------------------------
        # Section 2: Music & Audio Profile
        # -------------------------------------------------------------
        self.c_layout.addSpacing(8)
        self.c_layout.addWidget(self._create_section_label('MUSIC & AUDIO PROFILE'))

        audio_card = SettingCard(self.is_light)
        au_layout = QVBoxLayout(audio_card)
        au_layout.setContentsMargins(16, 14, 16, 14)
        au_layout.setSpacing(12)

        # Equalizer preset
        eq_row = QHBoxLayout()
        eq_texts = QVBoxLayout()
        eq_texts.setSpacing(2)
        eq_title = QLabel('Equalizer Sound Profile')
        eq_title.setStyleSheet('font-size: 14px; font-weight: 600;')
        eq_desc = QLabel('Native LibVLC 4 acoustic frequency curve for music and video playback')
        eq_desc.setStyleSheet('font-size: 12px; color: #888888;')
        eq_texts.addWidget(eq_title)
        eq_texts.addWidget(eq_desc)
        eq_row.addLayout(eq_texts, 1)

        self.eq_combo = QComboBox()
        self.eq_combo.setMinimumWidth(220)
        for code, name in self.EQUALIZER_PRESETS:
            self.eq_combo.addItem(name, code)
        self.eq_combo.currentIndexChanged.connect(self._on_eq_combo_changed)
        eq_row.addWidget(self.eq_combo)
        au_layout.addLayout(eq_row)

        # Auto-resume playback position
        resume_row = QHBoxLayout()
        resume_texts = QVBoxLayout()
        resume_texts.setSpacing(2)
        resume_title = QLabel('Resume Playback')
        resume_title.setStyleSheet('font-size: 14px; font-weight: 600;')
        resume_desc = QLabel('Remember and resume exact playback timestamp when reopening tracks')
        resume_desc.setStyleSheet('font-size: 12px; color: #888888;')
        resume_texts.addWidget(resume_title)
        resume_texts.addWidget(resume_desc)
        resume_row.addLayout(resume_texts, 1)

        self.resume_cb = FluentToggleSwitch(self, is_light=self.is_light, accent=accent, accent_text=accent_text)
        self.resume_cb.toggled.connect(lambda v: self._save_bool_setting('auto_resume', v))
        resume_row.addWidget(self.resume_cb)
        au_layout.addLayout(resume_row)

        self.c_layout.addWidget(audio_card)

        # -------------------------------------------------------------
        # Section 3: Video Settings
        # -------------------------------------------------------------
        self.c_layout.addSpacing(8)
        self.c_layout.addWidget(self._create_section_label('VIDEO PLAYBACK'))

        video_card = SettingCard(self.is_light)
        v_layout = QVBoxLayout(video_card)
        v_layout.setContentsMargins(16, 14, 16, 14)
        v_layout.setSpacing(12)

        # Aspect ratio
        ar_row = QHBoxLayout()
        ar_texts = QVBoxLayout()
        ar_texts.setSpacing(2)
        ar_title = QLabel('Default Aspect Ratio')
        ar_title.setStyleSheet('font-size: 14px; font-weight: 600;')
        ar_desc = QLabel('Screen scaling ratio for video playback')
        ar_desc.setStyleSheet('font-size: 12px; color: #888888;')
        ar_texts.addWidget(ar_title)
        ar_texts.addWidget(ar_desc)
        ar_row.addLayout(ar_texts, 1)

        self.ar_combo = QComboBox()
        self.ar_combo.setMinimumWidth(220)
        for code, name in self.ASPECT_RATIOS:
            self.ar_combo.addItem(name, code)
        self.ar_combo.currentIndexChanged.connect(self._on_ar_combo_changed)
        ar_row.addWidget(self.ar_combo)
        v_layout.addLayout(ar_row)

        # Hardware acceleration
        hw_row = QHBoxLayout()
        hw_texts = QVBoxLayout()
        hw_texts.setSpacing(2)
        hw_title = QLabel('Hardware Acceleration')
        hw_title.setStyleSheet('font-size: 14px; font-weight: 600;')
        hw_desc = QLabel('Use GPU hardware decoding for ultra-smooth 4K/60fps video output')
        hw_desc.setStyleSheet('font-size: 12px; color: #888888;')
        hw_texts.addWidget(hw_title)
        hw_texts.addWidget(hw_desc)
        hw_row.addLayout(hw_texts, 1)

        self.hw_cb = FluentToggleSwitch(self, is_light=self.is_light, accent=accent, accent_text=accent_text)
        self.hw_cb.toggled.connect(lambda v: self._save_bool_setting('hardware_decoding', v))
        hw_row.addWidget(self.hw_cb)
        v_layout.addLayout(hw_row)

        self.c_layout.addWidget(video_card)

        # -------------------------------------------------------------
        # Section 4: Windows Default Apps & System Integration
        # -------------------------------------------------------------
        self.c_layout.addSpacing(8)
        self.c_layout.addWidget(self._create_section_label('DEFAULT APPS & SYSTEM INTEGRATION'))

        default_card = SettingCard(self.is_light)
        d_layout = QVBoxLayout(default_card)
        d_layout.setContentsMargins(16, 14, 16, 14)
        d_layout.setSpacing(12)

        d_row = QHBoxLayout()
        d_texts = QVBoxLayout()
        d_texts.setSpacing(2)
        d_title = QLabel('Default Media Player')
        d_title.setStyleSheet('font-size: 14px; font-weight: 600;')
        d_desc = QLabel('Register Ocal Media Player in Windows 11 Default Apps with thumbnail previews and native file icons')
        d_desc.setStyleSheet('font-size: 12px; color: #888888;')
        d_texts.addWidget(d_title)
        d_texts.addWidget(d_desc)
        d_row.addLayout(d_texts, 1)

        self.set_default_btn = QPushButton('Set as Default Player')
        self.set_default_btn.setObjectName('dialogPrimary')
        self.set_default_btn.clicked.connect(self._on_set_default_player)
        d_row.addWidget(self.set_default_btn)

        self.open_default_settings_btn = QPushButton('Open Windows Default Apps')
        self.open_default_settings_btn.clicked.connect(open_windows_default_apps_settings)
        d_row.addWidget(self.open_default_settings_btn)

        d_layout.addLayout(d_row)

        self.default_status_lbl = QLabel()
        self.default_status_lbl.setStyleSheet('font-size: 12px; color: #888888;')
        self._refresh_default_status()
        d_layout.addWidget(self.default_status_lbl)

        self.c_layout.addWidget(default_card)

        # -------------------------------------------------------------
        # Section 5: Updates & About
        # -------------------------------------------------------------
        self.c_layout.addSpacing(8)
        self.c_layout.addWidget(self._create_section_label('SOFTWARE UPDATES & STORAGE'))

        update_card = SettingCard(self.is_light)
        u_layout = QVBoxLayout(update_card)
        u_layout.setContentsMargins(16, 14, 16, 14)
        u_layout.setSpacing(12)

        # Version & Check Button Row
        u_row = QHBoxLayout()
        u_texts = QVBoxLayout()
        u_texts.setSpacing(2)
        u_title = QLabel('Ocal Media Player')
        u_title.setStyleSheet('font-size: 14px; font-weight: 600;')
        self.version_lbl = QLabel(f'Version {CURRENT_VERSION}  ·  Developer: Ocal Software under Gaming Network Studio')
        self.version_lbl.setStyleSheet('font-size: 12px; color: #888888;')
        u_texts.addWidget(u_title)
        u_texts.addWidget(self.version_lbl)
        u_row.addLayout(u_texts, 1)

        self.check_update_btn = QPushButton('Check for updates')
        self.check_update_btn.setObjectName('dialogPrimary')
        self.check_update_btn.clicked.connect(self.check_for_updates)
        u_row.addWidget(self.check_update_btn)
        u_layout.addLayout(u_row)

        # Update Status & Action Card (Initially hidden or showing up to date)
        self.update_status_box = QFrame()
        self.update_status_box.setStyleSheet('background: rgba(0, 0, 0, 0.15); border-radius: 6px; padding: 10px;')
        s_box_layout = QVBoxLayout(self.update_status_box)
        s_box_layout.setContentsMargins(8, 8, 8, 8)
        s_box_layout.setSpacing(6)

        self.update_status_lbl = QLabel(f'Ocal Media Player is currently up to date (v{CURRENT_VERSION}).')
        self.update_status_lbl.setStyleSheet('font-size: 12px;')
        s_box_layout.addWidget(self.update_status_lbl)

        self.update_progress = QProgressBar()
        self.update_progress.setFixedHeight(6)
        self.update_progress.setTextVisible(False)
        self.update_progress.setVisible(False)
        s_box_layout.addWidget(self.update_progress)

        self.install_update_btn = QPushButton('Download and Install Update')
        self.install_update_btn.setObjectName('dialogPrimary')
        self.install_update_btn.setVisible(False)
        self.install_update_btn.clicked.connect(self._download_and_install_update)
        s_box_layout.addWidget(self.install_update_btn)

        u_layout.addWidget(self.update_status_box)

        # Storage directory row
        stor_row = QHBoxLayout()
        stor_texts = QVBoxLayout()
        stor_texts.setSpacing(2)
        stor_title = QLabel('Library Storage')
        stor_title.setStyleSheet('font-size: 13px; font-weight: 600;')
        self.stor_path_lbl = QLabel(str(self.library.directory))
        self.stor_path_lbl.setStyleSheet('font-size: 11px; color: #888888;')
        self.stor_path_lbl.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        stor_texts.addWidget(stor_title)
        stor_texts.addWidget(self.stor_path_lbl)
        stor_row.addLayout(stor_texts, 1)

        open_folder_btn = QPushButton('Open folder')
        open_folder_btn.clicked.connect(self._open_storage_folder)
        stor_row.addWidget(open_folder_btn)
        u_layout.addLayout(stor_row)

        self.c_layout.addWidget(update_card)
        self.c_layout.addStretch(1)

        self.scroll.setWidget(container)
        root_layout.addWidget(self.scroll)

    def _create_section_label(self, text):
        lbl = QLabel(text)
        lbl.setStyleSheet('font-size: 11px; font-weight: 700; color: #888888; letter-spacing: 1.2px; margin-top: 8px;')
        return lbl

    def load_settings(self):
        """Populate settings controls from library.settings."""
        s = self.library.settings

        # Theme Mode
        mode = s.get('theme_mode', 'system')
        if mode == 'dark':
            self.theme_combo.setCurrentIndex(1)
        elif mode == 'light':
            self.theme_combo.setCurrentIndex(2)
        else:
            self.theme_combo.setCurrentIndex(0)

        # Accent Color
        curr_accent = s.get('accent_color', 'system')
        self._update_swatch_selection(curr_accent)

        # Audio Equalizer
        eq = s.get('audio_profile', 'Flat')
        idx = self.eq_combo.findData(eq)
        if idx >= 0:
            self.eq_combo.setCurrentIndex(idx)

        # Auto resume
        self.resume_cb.setChecked(s.get('auto_resume', True))

        # Video aspect
        ar = s.get('video_aspect', 'Auto')
        idx = self.ar_combo.findData(ar)
        if idx >= 0:
            self.ar_combo.setCurrentIndex(idx)

        # Hardware decoding
        self.hw_cb.setChecked(s.get('hardware_decoding', True))

        # Recently played visibility
        show_recent = s.get('show_recently_played', True)
        if 'hide_recent_view' in s:
            show_recent = not s['hide_recent_view']
        self.show_recent_cb.setChecked(show_recent)

    def _update_swatch_selection(self, selected_hex):
        found = False
        for hex_code, btn in self.swatch_buttons:
            is_match = (hex_code.lower() == selected_hex.lower())
            btn.setSelected(is_match)
            if is_match:
                found = True
        if not found and selected_hex != 'system':
            self.hex_input.setText(selected_hex)
        else:
            self.hex_input.clear()

    def _on_theme_combo_changed(self, index):
        modes = ['system', 'dark', 'light']
        mode = modes[index] if 0 <= index < len(modes) else 'system'
        self.library.settings['theme_mode'] = mode
        self.library.save()
        self.theme_mode_changed.emit(mode)

    def _select_accent_color(self, hex_code):
        self.library.settings['accent_color'] = hex_code
        self.library.save()
        self._update_swatch_selection(hex_code)
        pal = make_accent_palette(hex_code, self.is_light) if hex_code != 'system' else get_windows_accent_palette(self.is_light)
        for switch in self.findChildren(FluentToggleSwitch):
            switch.apply_theme(self.is_light, pal['accent'], pal.get('text', '#ffffff'))
        self.accent_color_changed.emit(hex_code)

    def _apply_custom_hex(self):
        txt = self.hex_input.text().strip()
        if not txt.startswith('#'):
            txt = '#' + txt
        if len(txt) == 7:
            try:
                int(txt[1:], 16)
                self._select_accent_color(txt)
            except ValueError:
                pass

    def _on_eq_combo_changed(self, index):
        code = self.eq_combo.itemData(index)
        if code:
            self.library.settings['audio_profile'] = code
            self.library.save()
            self.audio_profile_changed.emit(code)
            if self.engine:
                self.engine.set_equalizer_preset(code)

    def _on_ar_combo_changed(self, index):
        code = self.ar_combo.itemData(index)
        if code:
            self.library.settings['video_aspect'] = code
            self.library.save()
            self.video_aspect_changed.emit(code)
            if self.engine:
                self.engine.set_aspect_ratio(code)

    def _on_recent_view_toggled(self, checked):
        self.library.settings['show_recently_played'] = bool(checked)
        self.library.settings['hide_recent_view'] = not bool(checked)
        self.library.save()
        self.setting_saved.emit('show_recently_played', bool(checked))
        self.setting_saved.emit('hide_recent_view', not bool(checked))

    def _save_bool_setting(self, key, value):
        self.library.settings[key] = bool(value)
        self.library.save()
        self.setting_saved.emit(key, value)

    def _open_storage_folder(self):
        try:
            os.startfile(str(self.library.directory))
        except Exception:
            subprocess.Popen(['explorer', str(self.library.directory)])

    def _on_set_default_player(self):
        """Register Ocal Media Player in Windows Default Apps and open settings."""
        register_default_media_player()
        self._refresh_default_status()
        open_windows_default_apps_settings()

    def _refresh_default_status(self):
        """Update Default Apps status label."""
        if hasattr(self, 'default_status_lbl'):
            if is_registered_in_default_apps():
                self.default_status_lbl.setText('✓ Registered in Windows Default Apps (14 file types: MP3, MP4, FLAC, MKV, WAV, M4A, etc.)')
                self.default_status_lbl.setStyleSheet('font-size: 12px; color: #10b981;')
            else:
                self.default_status_lbl.setText('Ocal Media Player is not currently registered in Windows Default Apps.')
                self.default_status_lbl.setStyleSheet('font-size: 12px; color: #888888;')

    def check_for_updates(self):
        """Initiate background update check."""
        self.check_update_btn.setEnabled(False)
        self.update_status_lbl.setText('Checking for updates from GitHub releases...')
        self.update_progress.setVisible(False)
        self.install_update_btn.setVisible(False)

        self.checker_thread = UpdateCheckerThread(self, current_version=CURRENT_VERSION)
        self.checker_thread.update_available.connect(self._on_update_available)
        self.checker_thread.up_to_date.connect(self._on_up_to_date)
        self.checker_thread.error.connect(self._on_update_check_error)
        self.checker_thread.start()

    def _on_update_available(self, version, notes, download_url, asset_name):
        self.check_update_btn.setEnabled(True)
        self.update_target_url = download_url
        self.update_target_asset = asset_name
        self.update_status_lbl.setText(f'A new update is available: v{version}\nRelease notes: {notes}')
        if download_url:
            self.install_update_btn.setText(f'Download & Install v{version}')
            self.install_update_btn.setVisible(True)

    def _on_up_to_date(self, current_ver):
        self.check_update_btn.setEnabled(True)
        self.update_status_lbl.setText(f'Ocal Media Player is currently up to date (v{current_ver}).')

    def _on_update_check_error(self, err_msg):
        self.check_update_btn.setEnabled(True)
        self.update_status_lbl.setText(f'Could not reach update server: {err_msg}')

    def _download_and_install_update(self):
        if not getattr(self, 'update_target_url', None):
            return
        self.install_update_btn.setEnabled(False)
        self.update_progress.setValue(0)
        self.update_progress.setVisible(True)
        self.update_status_lbl.setText(f'Downloading {self.update_target_asset}...')

        self.downloader_thread = UpdateDownloaderThread(self.update_target_url, self.update_target_asset, self)
        self.downloader_thread.progress.connect(self.update_progress.setValue)
        self.downloader_thread.finished.connect(self._on_download_finished)
        self.downloader_thread.error.connect(self._on_download_error)
        self.downloader_thread.start()

    def _on_download_finished(self, target_path):
        self.update_status_lbl.setText('Download complete! Launching installer and updating...')
        self.update_progress.setValue(100)
        launch_installer_and_exit(target_path, silent=False)

    def _on_download_error(self, err_msg):
        self.install_update_btn.setEnabled(True)
        self.update_progress.setVisible(False)
        self.update_status_lbl.setText(f'Update download failed: {err_msg}')

    def apply_theme(self, is_light, palette):
        """Update settings cards and labels when application theme changes."""
        self.is_light = is_light
        self.palette_data = palette
        win_pal = get_windows_accent_palette(is_light)
        for card in self.findChildren(SettingCard):
            card.update_style(is_light)
        for hex_code, btn in self.swatch_buttons:
            if hex_code == 'system':
                btn.update_system_color(win_pal['accent'], win_pal.get('text', '#ffffff'))
            else:
                btn.update()
        for switch in self.findChildren(FluentToggleSwitch):
            switch.apply_theme(is_light, palette['accent'], palette.get('text', '#ffffff'))

