"""Native Windows 11 Fluent ContentDialogs for Ocal Media Player."""
from pathlib import Path
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QWidget, QFrame, QGridLayout, QLineEdit, QApplication, QSizePolicy
)
from PySide6.QtCore import Qt, QRect, QRectF
from PySide6.QtGui import QPainter, QColor, QFont, QPen, QBrush, QPainterPath

from .win11 import (
    apply_win11_attributes, get_windows_accent_palette, is_windows_light_theme,
    WIN11_ACCENT, WIN11_ACCENT_HOVER, WIN11_ACCENT_PRESSED,
    WIN11_ACCENT_BASE, WIN11_ACCENT_TEXT, WIN11_ACCENT_RGB
)
from .icons import get_icon


class FluentBadge(QWidget):
    """Accent-tinted or gradient icon badge for Windows 11 dialog headers."""
    def __init__(self, icon_name='info', use_gradient=False, size=46, parent=None, is_light=None):
        super().__init__(parent)
        self.icon_name = icon_name
        self.use_gradient = use_gradient
        self.size_px = size
        self.setFixedSize(size, size)
        if is_light is None:
            is_light = is_windows_light_theme()
        self.is_light = is_light
        self.palette_data = get_windows_accent_palette(is_light)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = QRectF(1, 1, self.size_px - 2, self.size_px - 2)

        if self.use_gradient:
            # Gradient from accent to base accent (Windows Media Player brand badge)
            path = QPainterPath()
            path.addRoundedRect(rect, 10, 10)
            p.fillPath(path, QColor(self.palette_data['accent']))
            # Draw icon in contrasting text color
            icon = get_icon(self.icon_name, self.palette_data['text'], 22)
            icon_rect = QRect((self.size_px - 22) // 2 + 1, (self.size_px - 22) // 2, 22, 22)
            icon.paint(p, icon_rect)
        else:
            # Tinted background with accent outline
            r, g, b = self.palette_data['rgb']
            p.setBrush(QColor(r, g, b, 40))
            p.setPen(QPen(QColor(r, g, b, 90), 1))
            p.drawRoundedRect(rect, 10, 10)

            icon = get_icon(self.icon_name, self.palette_data['accent'], 22)
            icon_rect = QRect((self.size_px - 22) // 2, (self.size_px - 22) // 2, 22, 22)
            icon.paint(p, icon_rect)
        p.end()


class FluentDialog(QDialog):
    """Windows 11 Fluent ContentDialog styled to match the active OS accent color theme."""
    def __init__(self, parent=None, title='Media Player', is_light=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setMinimumWidth(480)
        if is_light is None:
            is_light = is_windows_light_theme()
        self.is_light = is_light
        self.palette_data = get_windows_accent_palette(is_light)

        if is_light:
            bg = '#f3f3f3'
            text_title = '#111111'
            text_body = '#2b2b2b'
            text_muted = '#616161'
            sep = 'rgba(0, 0, 0, 0.08)'
            sec_btn_bg = 'rgba(0, 0, 0, 0.04)'
            sec_btn_border = '1px solid rgba(0, 0, 0, 0.10)'
            sec_btn_color = '#1b1b1b'
            sec_btn_hover = 'rgba(0, 0, 0, 0.08)'
            badge_bg = 'rgba(0, 0, 0, 0.05)'
            badge_border = '1px solid rgba(0, 0, 0, 0.10)'
            input_bg = '#ffffff'
            input_border = '1px solid rgba(0, 0, 0, 0.14)'
            input_color = '#111111'
            input_focus = '#ffffff'
        else:
            bg = '#242424'
            text_title = '#ffffff'
            text_body = '#cccccc'
            text_muted = '#909090'
            sep = 'rgba(255, 255, 255, 0.08)'
            sec_btn_bg = 'rgba(255, 255, 255, 0.06)'
            sec_btn_border = '1px solid rgba(255, 255, 255, 0.08)'
            sec_btn_color = '#ffffff'
            sec_btn_hover = 'rgba(255, 255, 255, 0.10)'
            badge_bg = 'rgba(255, 255, 255, 0.08)'
            badge_border = '1px solid rgba(255, 255, 255, 0.12)'
            input_bg = 'rgba(255, 255, 255, 0.06)'
            input_border = '1px solid rgba(255, 255, 255, 0.12)'
            input_color = '#ffffff'
            input_focus = 'rgba(255, 255, 255, 0.09)'

        self.setObjectName('fluentDialog')
        self.setStyleSheet(f"""
            QDialog#fluentDialog {{
                background: {bg};
                color: {text_title};
            }}
            QLabel#dialogTitle {{
                font-size: 17px;
                font-weight: 600;
                color: {text_title};
                letter-spacing: -0.3px;
                margin: 0px;
                padding: 0px;
            }}
            QLabel#dialogSubtitle {{
                font-size: 10px;
                font-weight: 700;
                color: {self.palette_data['accent']};
                letter-spacing: 1.2px;
                margin: 0px;
                padding: 0px;
            }}
            QLabel#dialogBody {{
                font-size: 12px;
                color: {text_body};
                line-height: 1.4;
            }}
            QLabel#dialogMuted {{
                font-size: 11px;
                color: {text_muted};
            }}
            QFrame#dialogSeparator {{
                background: {sep};
                max-height: 1px;
                border: none;
            }}
            QPushButton#dialogPrimary {{
                background: {self.palette_data['accent']};
                color: {self.palette_data['text']};
                border: 1px solid {self.palette_data['accent']};
                border-radius: 6px;
                padding: 7px 24px;
                font-weight: 600;
                font-size: 12px;
                min-width: 80px;
            }}
            QPushButton#dialogPrimary:hover {{
                background: {self.palette_data['hover']};
                border-color: {self.palette_data['hover']};
            }}
            QPushButton#dialogPrimary:pressed {{
                background: {self.palette_data['pressed']};
                border-color: {self.palette_data['pressed']};
            }}
            QPushButton#dialogSecondary {{
                background: {sec_btn_bg};
                color: {sec_btn_color};
                border: {sec_btn_border};
                border-radius: 6px;
                padding: 7px 20px;
                font-weight: 500;
                font-size: 12px;
                min-width: 80px;
            }}
            QPushButton#dialogSecondary:hover {{
                background: {sec_btn_hover};
            }}
            QFrame#shortcutBadge {{
                background: {badge_bg};
                border: {badge_border};
                border-radius: 5px;
                padding: 4px 8px;
            }}
            QLabel#shortcutKey {{
                font-family: 'Segoe UI', 'Consolas', sans-serif;
                font-size: 11px;
                font-weight: 600;
                color: {self.palette_data['accent']};
            }}
            QLineEdit#dialogInput {{
                background: {input_bg};
                border: {input_border};
                border-radius: 6px;
                padding: 8px 12px;
                color: {input_color};
                font-size: 12px;
            }}
            QLineEdit#dialogInput:focus {{
                border: 2px solid {self.palette_data['accent']};
                background: {input_focus};
            }}
        """)

    def showEvent(self, event):
        super().showEvent(event)
        # Apply Windows 11 rounded corners, matching caption and dark/light titlebar
        apply_win11_attributes(self, is_light=self.is_light)

    @classmethod
    def about(cls, parent, vlc_version='4.0.0-dev', storage_dir=''):
        """Display Windows 11 About ContentDialog styled with active system accent."""
        dlg = cls(parent, title='Ocal Media Player')
        layout = QVBoxLayout(dlg)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Header
        header = QHBoxLayout()
        header.setContentsMargins(0, 0, 0, 0)
        header.setSpacing(14)
        header.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        badge = FluentBadge('play', use_gradient=True, size=46)
        header.addWidget(badge)

        h_texts = QVBoxLayout()
        h_texts.setContentsMargins(0, 0, 0, 0)
        h_texts.setSpacing(1)
        h_texts.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        sub = QLabel('OCAL MEDIA PLAYER')
        sub.setObjectName('dialogSubtitle')
        sub.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        h_texts.addWidget(sub)
        title = QLabel('Ocal Media Player')
        title.setObjectName('dialogTitle')
        title.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        h_texts.addWidget(title)
        header.addLayout(h_texts, 1)
        layout.addLayout(header)

        # Separator
        sep = QFrame()
        sep.setObjectName('dialogSeparator')
        layout.addWidget(sep)

        # Body
        body = QVBoxLayout()
        body.setSpacing(10)

        clean_vlc = str(vlc_version).strip()
        if 'Otto Chriek' not in clean_vlc:
            clean_vlc = f"{clean_vlc} Otto Chriek"

        intro = QLabel('A native Fluent Design desktop player built for Windows 11.\n'
                       'Developer: Ocal Software under Gaming Network Studio\n'
                       f'Powered by LibVLC {clean_vlc}.')
        intro.setObjectName('dialogBody')
        intro.setWordWrap(True)
        body.addWidget(intro)

        # Storage Card
        storage_card = QFrame()
        storage_card.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.04);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 8px;
                padding: 10px 12px;
            }
        """)
        s_layout = QVBoxLayout(storage_card)
        s_layout.setContentsMargins(4, 4, 4, 4)
        s_layout.setSpacing(4)

        s_head = QLabel('LIBRARY STORAGE')
        s_head.setObjectName('dialogSubtitle')
        s_layout.addWidget(s_head)

        s_path = QLabel(str(storage_dir))
        s_path.setObjectName('dialogBody')
        s_path.setTextInteractionFlags(Qt.TextSelectableByMouse)
        s_path.setWordWrap(True)
        s_layout.addWidget(s_path)
        body.addWidget(storage_card)

        layout.addLayout(body)

        # Footer Action Bar
        footer = QHBoxLayout()
        footer.addStretch(1)

        ok_btn = QPushButton('OK')
        ok_btn.setObjectName('dialogPrimary')
        ok_btn.clicked.connect(dlg.accept)
        footer.addWidget(ok_btn)

        layout.addLayout(footer)
        ok_btn.setFocus()
        return dlg.exec()

    @classmethod
    def shortcuts(cls, parent):
        """Display Windows 11 Keyboard Shortcuts ContentDialog."""
        dlg = cls(parent, title='Keyboard Shortcuts')
        dlg.setMinimumWidth(500)
        layout = QVBoxLayout(dlg)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Header
        header = QHBoxLayout()
        header.setContentsMargins(0, 0, 0, 0)
        header.setSpacing(14)
        header.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        badge = FluentBadge('keyboard', use_gradient=False, size=46)
        header.addWidget(badge)

        h_texts = QVBoxLayout()
        h_texts.setContentsMargins(0, 0, 0, 0)
        h_texts.setSpacing(1)
        h_texts.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        sub = QLabel('QUICK REFERENCE')
        sub.setObjectName('dialogSubtitle')
        sub.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        h_texts.addWidget(sub)
        title = QLabel('Keyboard Shortcuts')
        title.setObjectName('dialogTitle')
        title.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        h_texts.addWidget(title)
        header.addLayout(h_texts, 1)
        layout.addLayout(header)

        # Separator
        sep = QFrame()
        sep.setObjectName('dialogSeparator')
        layout.addWidget(sep)

        # Shortcuts Grid
        items = [
            ('Ctrl + O', 'Open media files'),
            ('Ctrl + F', 'Search media library'),
            ('Space', 'Play or pause playback'),
            ('← / →', 'Seek 10s backward or forward'),
            ('M', 'Mute or unmute volume'),
            ('B', 'Bookmark current moment'),
            ('F11', 'Toggle full screen mode'),
            ('Esc', 'Exit full screen mode'),
        ]

        grid = QGridLayout()
        grid.setSpacing(8)
        grid.setColumnStretch(1, 1)

        for row, (key, desc) in enumerate(items):
            key_frame = QFrame()
            key_frame.setObjectName('shortcutBadge')
            k_layout = QHBoxLayout(key_frame)
            k_layout.setContentsMargins(8, 3, 8, 3)
            k_lbl = QLabel(key)
            k_lbl.setObjectName('shortcutKey')
            k_layout.addWidget(k_lbl)
            grid.addWidget(key_frame, row, 0, Qt.AlignmentFlag.AlignLeft)

            desc_lbl = QLabel(desc)
            desc_lbl.setObjectName('dialogBody')
            grid.addWidget(desc_lbl, row, 1, Qt.AlignmentFlag.AlignVCenter)

        layout.addLayout(grid)

        # Tip
        tip = QLabel('Tip: Drag & drop media files or folders anywhere into the window to import.')
        tip.setObjectName('dialogMuted')
        layout.addWidget(tip)

        # Footer
        footer = QHBoxLayout()
        footer.addStretch(1)

        ok_btn = QPushButton('Close')
        ok_btn.setObjectName('dialogPrimary')
        ok_btn.clicked.connect(dlg.accept)
        footer.addWidget(ok_btn)

        layout.addLayout(footer)
        ok_btn.setFocus()
        return dlg.exec()

    @classmethod
    def prompt_stream(cls, parent, default_url=''):
        """Prompt for a network stream URL using Windows 11 Fluent ContentDialog."""
        dlg = cls(parent, title='Open Network Stream')
        dlg.setMinimumWidth(500)
        layout = QVBoxLayout(dlg)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Header
        header = QHBoxLayout()
        header.setContentsMargins(0, 0, 0, 0)
        header.setSpacing(14)
        header.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        badge = FluentBadge('stream', use_gradient=False, size=46)
        header.addWidget(badge)

        h_texts = QVBoxLayout()
        h_texts.setContentsMargins(0, 0, 0, 0)
        h_texts.setSpacing(1)
        h_texts.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        sub = QLabel('NETWORK PLAYBACK')
        sub.setObjectName('dialogSubtitle')
        sub.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        h_texts.addWidget(sub)
        title = QLabel('Open Network Stream')
        title.setObjectName('dialogTitle')
        title.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        h_texts.addWidget(title)
        header.addLayout(h_texts, 1)
        layout.addLayout(header)

        # Separator
        sep = QFrame()
        sep.setObjectName('dialogSeparator')
        layout.addWidget(sep)

        # Body
        body = QVBoxLayout()
        body.setSpacing(8)

        lbl = QLabel('Enter the URL of the media stream to play:')
        lbl.setObjectName('dialogBody')
        body.addWidget(lbl)

        line_edit = QLineEdit(default_url)
        line_edit.setObjectName('dialogInput')
        line_edit.setPlaceholderText('https://example.com/live/stream.m3u8')
        line_edit.selectAll()
        body.addWidget(line_edit)

        supported = QLabel('Supported protocols: HTTP · HTTPS · RTSP · RTMP · UDP · RTP')
        supported.setObjectName('dialogMuted')
        body.addWidget(supported)

        layout.addLayout(body)

        # Footer
        footer = QHBoxLayout()
        footer.addStretch(1)

        cancel_btn = QPushButton('Cancel')
        cancel_btn.setObjectName('dialogSecondary')
        cancel_btn.clicked.connect(dlg.reject)
        footer.addWidget(cancel_btn)

        play_btn = QPushButton('Play')
        play_btn.setObjectName('dialogPrimary')
        play_btn.clicked.connect(dlg.accept)
        footer.addWidget(play_btn)

        line_edit.returnPressed.connect(dlg.accept)
        layout.addLayout(footer)
        line_edit.setFocus()

        res = dlg.exec()
        return line_edit.text().strip(), res == QDialog.DialogCode.Accepted

    @classmethod
    def message(cls, parent, title, subtitle, message, icon_name='info'):
        """Display an informational or warning Windows 11 Fluent ContentDialog."""
        dlg = cls(parent, title=title)
        layout = QVBoxLayout(dlg)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Header
        header = QHBoxLayout()
        header.setContentsMargins(0, 0, 0, 0)
        header.setSpacing(14)
        header.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        badge = FluentBadge(icon_name, use_gradient=False, size=46)
        header.addWidget(badge)

        h_texts = QVBoxLayout()
        h_texts.setContentsMargins(0, 0, 0, 0)
        h_texts.setSpacing(1)
        h_texts.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        sub = QLabel(subtitle.upper())
        sub.setObjectName('dialogSubtitle')
        sub.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        h_texts.addWidget(sub)
        t_lbl = QLabel(title)
        t_lbl.setObjectName('dialogTitle')
        t_lbl.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        h_texts.addWidget(t_lbl)
        header.addLayout(h_texts, 1)
        layout.addLayout(header)

        # Separator
        sep = QFrame()
        sep.setObjectName('dialogSeparator')
        layout.addWidget(sep)

        # Body
        msg_lbl = QLabel(message)
        msg_lbl.setObjectName('dialogBody')
        msg_lbl.setWordWrap(True)
        layout.addWidget(msg_lbl)

        # Footer
        footer = QHBoxLayout()
        footer.addStretch(1)

        ok_btn = QPushButton('OK')
        ok_btn.setObjectName('dialogPrimary')
        ok_btn.clicked.connect(dlg.accept)
        footer.addWidget(ok_btn)

        layout.addLayout(footer)
        ok_btn.setFocus()
        return dlg.exec()

