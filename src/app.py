import ctypes
import math
import random
import sys
import time
from ctypes import wintypes
from pathlib import Path

from PySide6.QtCore import (
    Qt, QTimer, QSize, QThread, Signal, QRect, QRectF, QStandardPaths,
    QEvent, QPoint, QPropertyAnimation, QEasingCurve
)
from PySide6.QtGui import (
    QColor, QFont, QFontDatabase, QPainter, QPainterPath, QPen, QBrush,
    QLinearGradient, QRadialGradient, QShortcut, QKeySequence, QIcon, QPixmap, QCursor
)
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFrame, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QGridLayout, QSizePolicy, QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView,
    QAbstractItemView, QListWidget, QListWidgetItem, QSlider, QComboBox,
    QFileDialog, QInputDialog, QMessageBox, QMenu, QStackedWidget,
)

from .engine import Engine, ROOT
from .library import Library, AUDIO, VIDEO, clock
from .theme import STYLE, get_stylesheet
from .win11 import (
    apply_win11_attributes, apply_win11_frameless_attributes, glyph,
    WIN11_ACCENT, WIN11_ACCENT_HOVER, WIN11_ACCENT_PRESSED,
    WIN11_ACCENT_BASE, WIN11_ACCENT_TEXT, WIN11_BG,
    is_windows_light_theme, get_windows_accent_palette, refresh_win11_theme,
    make_accent_palette
)
from .dialogs import FluentDialog
from .icons import get_icon
from .artwork import get_media_artwork, clear_artwork_cache
from .metadata import extract_media_metadata
from .settings_view import SettingsView
from .updater import CURRENT_VERSION


def label(text, name='', wrap=False):
    result = QLabel(text)
    if name:
        result.setObjectName(name)
    result.setWordWrap(wrap)
    return result


def button(text, callback, name='', tip=''):
    result = QPushButton(text)
    if name:
        result.setObjectName(name)
    result.setCursor(Qt.CursorShape.PointingHandCursor)
    result.setToolTip(tip or text)
    result.setAccessibleName(tip or text)
    result.clicked.connect(callback)
    return result


class MediaThumbnail(QWidget):
    """Windows 11 Media Player rounded thumbnail badge in transport bar."""
    def __init__(self, parent=None, is_light=False, accent=None):
        super().__init__(parent)
        self.setFixedSize(42, 42)
        self.kind = ''
        self.pixmap = None
        self.is_light = is_light
        self.accent = accent or WIN11_ACCENT

    def set_theme(self, is_light, accent=None):
        self.is_light = is_light
        if accent:
            self.accent = accent
        self.update()

    def set_media(self, kind, pixmap=None):
        self.kind = kind
        self.pixmap = pixmap
        self.update()

    def set_kind(self, kind):
        self.kind = kind
        self.pixmap = None
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect().adjusted(1, 1, -1, -1)
        path = QPainterPath()
        path.addRoundedRect(QRectF(rect), 6, 6)

        if self.pixmap and not self.pixmap.isNull():
            p.setClipPath(path)
            scaled = self.pixmap.scaled(
                42, 42,
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
            p.drawPixmap(0, 0, scaled)
            p.setClipping(False)
            p.setPen(QPen(QColor(0, 0, 0, 30) if self.is_light else QColor(255, 255, 255, 30), 1))
            p.drawPath(path)
        else:
            border_pen = QColor(0, 0, 0, 25) if self.is_light else QColor(255, 255, 255, 20)
            bg_col = QColor(235, 235, 235) if self.is_light else QColor(42, 42, 42)
            p.setPen(QPen(border_pen, 1))
            p.setBrush(bg_col)
            p.drawPath(path)

            icon_name = 'music'
            if self.kind == 'Video':
                icon_name = 'video'
            elif self.kind == 'Stream':
                icon_name = 'stream'

            accent = self.accent or WIN11_ACCENT
            icon = get_icon(icon_name, accent, 20)
            icon_rect = QRect(11, 11, 20, 20)
            icon.paint(p, icon_rect)
        p.end()


class FolderScan(QThread):
    found = Signal(list)
    failed = Signal(str)

    def __init__(self, directories):
        super().__init__()
        if isinstance(directories, (str, Path)):
            self.directories = [directories]
        else:
            self.directories = list(directories)

    def run(self):
        try:
            paths = []
            for directory in self.directories:
                d_path = Path(directory)
                if not d_path.is_dir():
                    continue
                try:
                    for path in d_path.rglob('*'):
                        if self.isInterruptionRequested():
                            return
                        try:
                            if path.is_file() and path.suffix.lower() in AUDIO | VIDEO:
                                paths.append(str(path))
                        except (OSError, PermissionError):
                            continue
                except (OSError, PermissionError):
                    continue
            self.found.emit(sorted(paths))
        except Exception as exc:
            self.failed.emit(str(exc))


class MetadataScanner(QThread):
    progress = Signal(int)
    finished_scan = Signal(int)

    def __init__(self, items):
        super().__init__()
        self.items = items

    def run(self):
        updated = 0
        for entry in list(self.items):
            if self.isInterruptionRequested():
                return
            path = entry.get('path', '')
            if '://' in path or not path:
                continue
            needs_duration = entry.get('duration', 0) <= 0
            needs_artist = not entry.get('artist')
            if needs_duration or needs_artist:
                dur, tags = extract_media_metadata(path)
                changed = False
                if dur > 0 and needs_duration:
                    entry['duration'] = dur
                    changed = True
                if tags.get('artist') and not entry.get('artist'):
                    entry['artist'] = tags['artist']
                    changed = True
                if tags.get('album') and not entry.get('album'):
                    entry['album'] = tags['album']
                if changed:
                    updated += 1
                    if updated % 10 == 0:
                        self.progress.emit(updated)
        self.finished_scan.emit(updated)


class PlayerWindow(QMainWindow):
    def __init__(self, library=None):
        super().__init__()
        self.library = library or Library()

        user_mode = self.library.settings.get('theme_mode', 'system')
        if user_mode == 'dark':
            self.is_light = False
        elif user_mode == 'light':
            self.is_light = True
        else:
            self.is_light = is_windows_light_theme()

        user_accent = self.library.settings.get('accent_color', 'system')
        if user_accent and user_accent.lower() != 'system':
            self.palette = make_accent_palette(user_accent, self.is_light)
        else:
            self.palette = get_windows_accent_palette(self.is_light)

        self._current_is_light = self.is_light
        self._current_accent = self.palette['accent']
        self.current = None
        self.queue = []
        self.queue_index = -1
        self.view = 'All media'
        self.filter_kind = 'All'
        self.collection_layout_mode = 'list'
        self.a = self.b = None
        self.pending_resume = 0
        self.has_played = False
        self.last_save = 0
        self.sleep_deadline = None
        self.scanner = None
        self.meta_scanner = None
        self.engine = None
        self.setWindowTitle('Ocal Media Player')
        icon_path = ROOT / 'assets' / 'app-icon.ico'
        if icon_path.is_file():
            self.setWindowIcon(QIcon(str(icon_path)))
        self.resize(1300, 840)
        self.setMinimumSize(1020, 720)
        self.setWindowFlags(
            Qt.WindowType.Window
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowMinMaxButtonsHint
        )
        self.is_video_mode = False
        self.left_drawer_open = False
        self.right_drawer_open = False
        self.overlay_idle_timer = QTimer(self)
        self.overlay_idle_timer.setInterval(2500)
        self.overlay_idle_timer.setSingleShot(True)
        self.overlay_idle_timer.timeout.connect(self.on_overlay_idle_timeout)
        self.setAcceptDrops(True)
        self.build_ui()
        QApplication.instance().installEventFilter(self)
        # Apply native Windows 11 DWM dark/light mode, drop shadow, rounded corners
        apply_win11_frameless_attributes(self, self.is_light)
        self.engine = Engine(int(self.video.winId()))
        self.engine.volume(self.volume.value())

        # Apply saved equalizer profile and video aspect ratio
        if self.engine:
            self.engine.set_equalizer_preset(self.library.settings.get('audio_profile', 'Flat'))
            self.engine.set_aspect_ratio(self.library.settings.get('video_aspect', 'Auto'))

        self.status.setText('Ready · VLC 4 engine')
        self.bind_shortcuts()
        self.refresh()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.start(200)

        # Periodic live theme and accent color monitor
        self.theme_timer = QTimer(self)
        self.theme_timer.setInterval(1000)
        self.theme_timer.timeout.connect(self.check_system_theme)
        self.theme_timer.start()

        # Background metadata & duration scan for library items missing length
        if not self.library.is_custom:
            QTimer.singleShot(150, self.start_metadata_scan)
            if self.library.settings.get('auto_check_updates', True):
                QTimer.singleShot(3000, self.auto_check_updates)

        # Auto-discover media from Windows user media folders if running real app
        if not self.library.is_custom:
            QTimer.singleShot(400, self.auto_scan_media)

        if self.library.warning:
            QTimer.singleShot(0, lambda: FluentDialog.message(self, 'Library Recovery', 'Notice', self.library.warning))

    def showEvent(self, event):
        super().showEvent(event)
        apply_win11_frameless_attributes(self, self.is_light)

    def get_default_media_folders(self):
        """Retrieve standard Windows user media locations and custom watch folders."""
        folders = []
        for loc in (
            QStandardPaths.StandardLocation.MusicLocation,
            QStandardPaths.StandardLocation.MoviesLocation,
            QStandardPaths.StandardLocation.DownloadLocation,
        ):
            for path_str in QStandardPaths.standardLocations(loc):
                p = Path(path_str)
                if p.is_dir() and p not in folders:
                    folders.append(p)
        for custom_str in self.library.settings.get('watch_folders', []):
            cp = Path(custom_str)
            if cp.is_dir() and cp not in folders:
                folders.append(cp)
        return folders

    def auto_scan_media(self):
        folders = self.get_default_media_folders()
        if folders:
            self.status.setText('Scanning PC for music and video files…')
            self.scanner = FolderScan(folders)
            self.scanner.found.connect(self.on_auto_scan_found)
            self.scanner.start()

    def on_auto_scan_found(self, paths):
        if paths:
            self.library.add(paths)
            self.refresh()
            self.status.setText(f'Library ready: {len(self.library.items)} media files discovered.')
            self.start_metadata_scan()
        else:
            self.status.setText('Ready · VLC 4 engine')

    def start_metadata_scan(self):
        if self.meta_scanner and self.meta_scanner.isRunning():
            return
        needs_scan = any(
            x.get('duration', 0) <= 0 or not x.get('artist')
            for x in self.library.items
            if '://' not in x.get('path', '')
        )
        if needs_scan:
            self.meta_scanner = MetadataScanner(self.library.items)
            self.meta_scanner.progress.connect(self.on_metadata_batch)
            self.meta_scanner.finished_scan.connect(self.on_metadata_complete)
            self.meta_scanner.start()

    def on_metadata_batch(self, count):
        self.refresh()

    def on_metadata_complete(self, count):
        if count > 0:
            self.save()
            self.refresh()

    def scan_all_media(self):
        folders = self.get_default_media_folders()
        if not folders:
            self.status.setText('No media folders found to scan.')
            return
        if self.scanner and self.scanner.isRunning():
            self.status.setText('A library scan is already running.')
            return
        self.status.setText('Scanning PC for music and videos…')
        self.scanner = FolderScan(folders)
        self.scanner.found.connect(self.import_paths)
        self.scanner.failed.connect(lambda msg: self.status.setText('Scan failed: ' + msg))
        self.scanner.start()

    def build_ui(self):
        self.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent, True)
        self.canvas = QWidget(objectName='canvas')
        self.canvas.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent, True)
        self.canvas.setMouseTracking(True)
        self.setMouseTracking(True)
        self.setCentralWidget(self.canvas)
        self.outer_layout = QVBoxLayout(self.canvas)
        self.outer_layout.setContentsMargins(0, 0, 0, 0)
        self.outer_layout.setSpacing(0)

        self.body_layout = QHBoxLayout()
        self.body_layout.setSpacing(0)
        self.outer_layout.addLayout(self.body_layout, 1)

        # Left Sidebar (Windows 11 NavigationView)
        self.sidebar = QFrame(objectName='sidebar')
        self.sidebar.setFixedWidth(220)
        self.sidebar.setMouseTracking(True)
        side = QVBoxLayout(self.sidebar)
        side.setContentsMargins(12, 16, 12, 16)
        side.setSpacing(4)

        # Windows 11 App Header & Brand
        brand_row = QHBoxLayout()
        brand_row.setContentsMargins(4, 2, 4, 10)
        brand_row.setSpacing(10)

        accent = self.palette['accent']
        accent_base = self.palette.get('base', accent)
        accent_text = self.palette['text']
        nav_icon_color = '#444444' if self.is_light else '#cccccc'
        primary_icon = '#1b1b1b' if self.is_light else '#ffffff'
        cap_color = '#333333' if self.is_light else '#cccccc'

        self.icon_badge = QLabel()
        self.icon_badge.setFixedSize(26, 26)
        self.icon_badge.setStyleSheet(
            f'background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {accent}, stop:1 {accent_base});'
            'border-radius: 6px;'
        )
        p_pix = QPixmap(26, 26)
        p_pix.fill(Qt.GlobalColor.transparent)
        bp = QPainter(p_pix)
        bp.setRenderHint(QPainter.RenderHint.Antialiasing)
        get_icon('play', accent_text, 16).paint(bp, QRect(5, 5, 16, 16))
        bp.end()
        self.icon_badge.setPixmap(p_pix)
        brand_row.addWidget(self.icon_badge)

        self.brand_title = label('Ocal Media Player', 'brand')
        brand_row.addWidget(self.brand_title)
        brand_row.addStretch()
        side.addLayout(brand_row)

        side.addSpacing(6)
        side.addWidget(label('YOUR LIBRARY', 'eyebrow'))
        side.addSpacing(4)

        # Navigation items with vector icons
        self.nav = {}
        self.nav_icons = {
            'All media': 'home',
            'Music': 'music',
            'Videos': 'video',
            'Favorites': 'heart_fill',
            'Recently played': 'history',
            'Now playing': 'nowplaying',
            'Settings': 'settings',
        }
        nav_items = [
            ('All media', 'Home', 'home'),
            ('Music', 'Music library', 'music'),
            ('Videos', 'Video library', 'video'),
            ('Favorites', 'Favorites', 'heart_fill'),
            ('Recently played', 'Recently played', 'history'),
            ('Now playing', 'Now playing', 'nowplaying'),
        ]
        for key, display_text, icon_name in nav_items:
            b = button(display_text, lambda checked=False, t=key: self.navigate(t), 'nav')
            b.setIcon(get_icon(icon_name, nav_icon_color, 18))
            b.setCheckable(True)
            side.addWidget(b)
            self.nav[key] = b

        side.addStretch()

        self.sidebar_divider = QFrame()
        self.sidebar_divider.setFixedHeight(1)
        div_bg = 'rgba(0, 0, 0, 0.08)' if self.is_light else 'rgba(255, 255, 255, 0.08)'
        self.sidebar_divider.setStyleSheet(f'background: {div_bg}; margin: 6px 2px;')
        side.addWidget(self.sidebar_divider)

        self.settings_btn = button('Settings', lambda checked=False: self.navigate('Settings'), 'nav')
        self.settings_btn.setIcon(get_icon('settings', nav_icon_color, 18))
        self.settings_btn.setCheckable(True)
        side.addWidget(self.settings_btn)
        self.nav['Settings'] = self.settings_btn

        self.shortcuts_btn = button('Shortcuts', self.shortcuts_dialog, 'nav')
        self.shortcuts_btn.setIcon(get_icon('keyboard', nav_icon_color, 18))
        side.addWidget(self.shortcuts_btn)

        self.about_btn = button('About', self.about, 'nav')
        self.about_btn.setIcon(get_icon('info', nav_icon_color, 18))
        side.addWidget(self.about_btn)

        self.body_layout.addWidget(self.sidebar)

        # Main Content Layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(28, 16, 16, 14)
        self.main_layout.setSpacing(12)
        self.body_layout.addLayout(self.main_layout, 1)

        # Top CommandBar / Header & Windows 11 Caption Controls
        self.top_bar_widget = QWidget(objectName='top_bar_widget')
        top = QHBoxLayout(self.top_bar_widget)
        top.setContentsMargins(0, 0, 0, 0)
        top.setSpacing(10)

        self.heading = label('Home', 'heading')
        top.addWidget(self.heading)
        top.addStretch(1)

        self.search = QLineEdit()
        self.search.setPlaceholderText('Search music, videos, and playlists…')
        self.search.setAccessibleName('Search library')
        self.search.setFixedWidth(260)
        self.search.textChanged.connect(self.refresh)
        top.addWidget(self.search)

        self.open_btn = button('Open files', self.open_files, 'primary', 'Open files · Ctrl+O')
        self.open_btn.setIcon(get_icon('open_files', accent_text, 16))
        top.addWidget(self.open_btn)

        self.folder_button = button('Add folder', self.open_folder, '', 'Add media folder to library')
        self.folder_button.setIcon(get_icon('folder', primary_icon, 16))
        top.addWidget(self.folder_button)

        self.scan_btn = button('Scan PC', self.scan_all_media, '', 'Scan PC for all music and video files')
        self.scan_btn.setIcon(get_icon('refresh', primary_icon, 16))
        top.addWidget(self.scan_btn)

        self.stream_btn = button('Open stream', self.open_stream, '', 'Open network stream URL')
        self.stream_btn.setIcon(get_icon('stream', primary_icon, 16))
        top.addWidget(self.stream_btn)

        top.addSpacing(8)

        # Native Windows 11 Caption Controls (Minimize, Maximize, Close)
        caption_box = QHBoxLayout()
        caption_box.setContentsMargins(0, 0, 0, 0)
        caption_box.setSpacing(0)

        self.min_btn = button('', self.showMinimized, 'caption_btn', 'Minimize')
        self.min_btn.setIcon(get_icon('cap_min', cap_color, 12))
        caption_box.addWidget(self.min_btn)

        self.max_btn = button('', self.toggle_max, 'caption_btn', 'Maximize')
        self.max_btn.setIcon(get_icon('cap_max', cap_color, 12))
        caption_box.addWidget(self.max_btn)

        self.close_btn = button('', self.close, 'caption_close', 'Close')
        self.close_btn.setIcon(get_icon('cap_close', cap_color, 12))
        caption_box.addWidget(self.close_btn)

        self.caption_container = QWidget()
        self.caption_container.setLayout(caption_box)
        top.addWidget(self.caption_container)

        self.main_layout.addWidget(self.top_bar_widget)

        # Content Area: Collection Table & Queue Panel
        self.content_layout = QHBoxLayout()
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(16)
        self.main_layout.addLayout(self.content_layout, 1)

        self.pages = QStackedWidget()
        self.content_layout.addWidget(self.pages, 1)

        # Page 0: Library page (Full height desktop layout, no web landing hero banner)
        library_page = QWidget()
        lib = QVBoxLayout(library_page)
        lib.setContentsMargins(0, 0, 0, 0)
        lib.setSpacing(0)

        collection = QFrame(objectName='card')
        col = QVBoxLayout(collection)
        col.setContentsMargins(20, 16, 20, 12)
        col.setSpacing(12)

        collection_top = QHBoxLayout()
        collection_top.addWidget(label('The collection', 'section'))
        self.count = label('0 items', 'muted')
        collection_top.addWidget(self.count)
        collection_top.addStretch()

        self.chips = []
        for kind in ('All', 'Video', 'Music'):
            chip = button(kind, lambda checked=False, k=kind: self.set_filter(k), 'chip')
            chip.setCheckable(True)
            chip.setChecked(kind == 'All')
            self.chips.append(chip)
            collection_top.addWidget(chip)

        collection_top.addSpacing(6)

        # List and Grid View switchers
        self.btn_view_list = button('', lambda: self.set_collection_view('list'), 'view_toggle', 'List view')
        self.btn_view_list.setIcon(get_icon('view_list', accent_text, 16))
        self.btn_view_list.setCheckable(True)
        self.btn_view_list.setChecked(True)
        collection_top.addWidget(self.btn_view_list)

        self.btn_view_grid = button('', lambda: self.set_collection_view('grid'), 'view_toggle', 'Grid view')
        self.btn_view_grid.setIcon(get_icon('view_grid', '#a0a0a0', 16))
        self.btn_view_grid.setCheckable(True)
        collection_top.addWidget(self.btn_view_grid)

        col.addLayout(collection_top)

        self.collection_stack = QStackedWidget()

        # Page 0: List View (Table)
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.table.setIconSize(QSize(36, 36))
        self.table.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.table.setHorizontalHeaderLabels(['TITLE', 'ARTIST', 'TYPE', 'LENGTH', 'FAV'])

        h_title = self.table.horizontalHeaderItem(0)
        if h_title:
            h_title.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        h_artist = self.table.horizontalHeaderItem(1)
        if h_artist:
            h_artist.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        h_type = self.table.horizontalHeaderItem(2)
        if h_type:
            h_type.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        h_len = self.table.horizontalHeaderItem(3)
        if h_len:
            h_len.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        h_fav = self.table.horizontalHeaderItem(4)
        if h_fav:
            h_fav.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.setColumnWidth(1, 160)
        self.table.setColumnWidth(2, 80)
        self.table.setColumnWidth(3, 80)
        self.table.setColumnWidth(4, 52)
        self.table.verticalHeader().hide()
        self.table.verticalHeader().setDefaultSectionSize(48)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setShowGrid(False)
        self.table.cellDoubleClicked.connect(self.table_play)
        self.table.cellClicked.connect(self.table_cell_clicked)
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.library_menu)
        self.collection_stack.addWidget(self.table)

        # Page 1: Grid View (Artwork Cards)
        self.grid_view = QListWidget(objectName='grid_view')
        self.grid_view.setViewMode(QListWidget.ViewMode.IconMode)
        self.grid_view.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.grid_view.setGridSize(QSize(170, 220))
        self.grid_view.setIconSize(QSize(140, 140))
        self.grid_view.setSpacing(12)
        self.grid_view.setWordWrap(True)
        self.grid_view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.grid_view.itemDoubleClicked.connect(self.grid_play)
        self.grid_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.grid_view.customContextMenuRequested.connect(self.grid_menu)
        self.collection_stack.addWidget(self.grid_view)

        col.addWidget(self.collection_stack, 1)

        self.empty = label('Your next favorite belongs here.\nOpen files, add folders, or click Scan PC to start.', 'muted', True)
        self.empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        col.addWidget(self.empty)

        self.collection_hint = label('Double-click to play  ·  Right-click for queue, favorites & bookmarks', 'muted')
        col.addWidget(self.collection_hint)
        lib.addWidget(collection, 1)
        self.pages.addWidget(library_page)

        # Page 1: Now playing (Video) page
        playing_page = QWidget()
        playing = QVBoxLayout(playing_page)
        playing.setContentsMargins(0, 0, 0, 0)
        playing.setSpacing(12)

        self.video = QFrame()
        self.video.setStyleSheet('background: #000000; border: none; border-radius: 0px;')
        self.video.setAttribute(Qt.WidgetAttribute.WA_NativeWindow)
        self.video.setMouseTracking(True)
        self.video.setMinimumHeight(280)
        playing.addWidget(self.video, 1)

        # Center Music Stage for Audio tracks on Now playing page
        self.music_stage = QWidget()
        ms_layout = QVBoxLayout(self.music_stage)
        ms_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ms_layout.setContentsMargins(32, 32, 32, 32)
        ms_layout.setSpacing(14)

        self.music_now_art = QLabel()
        self.music_now_art.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.music_now_art.setFixedSize(220, 220)
        ms_layout.addWidget(self.music_now_art, 0, Qt.AlignmentFlag.AlignCenter)

        self.music_now_title = label('No track playing', 'section')
        self.music_now_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.music_now_title.setStyleSheet('font-size: 22px; font-weight: 700;')
        ms_layout.addWidget(self.music_now_title)

        self.music_now_artist = label('Select music from library to play', 'muted')
        self.music_now_artist.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.music_now_artist.setStyleSheet('font-size: 14px;')
        ms_layout.addWidget(self.music_now_artist)

        playing.addWidget(self.music_stage, 1)
        self.music_stage.hide()

        self.video_info_container = QWidget()
        video_info_row = QHBoxLayout(self.video_info_container)
        video_info_row.setContentsMargins(16, 10, 16, 10)
        v_copy = QVBoxLayout()
        self.playing_title = label('Choose something to play', 'section')
        v_copy.addWidget(self.playing_title)
        v_copy.addWidget(label('F11 for full screen · Space to pause · ← / → to seek', 'muted'))
        video_info_row.addLayout(v_copy, 1)

        muted_icon = '#666666' if self.is_light else '#a0a0a0'
        video_tools = QHBoxLayout()
        self.sub_btn = button('Subtitles', self.load_subtitles, 'chip')
        self.sub_btn.setIcon(get_icon('subtitles', muted_icon, 16))
        video_tools.addWidget(self.sub_btn)

        self.snap_btn = button('Snapshot', self.snapshot, 'chip')
        self.snap_btn.setIcon(get_icon('camera', muted_icon, 16))
        video_tools.addWidget(self.snap_btn)

        self.bm_btn = button('Bookmark', self.add_bookmark, 'chip')
        self.bm_btn.setIcon(get_icon('bookmark', muted_icon, 16))
        video_tools.addWidget(self.bm_btn)

        self.fs_tool = button('Fullscreen', self.fullscreen, 'chip')
        self.fs_tool.setIcon(get_icon('fullscreen', muted_icon, 16))
        video_tools.addWidget(self.fs_tool)

        video_info_row.addLayout(video_tools)
        playing.addWidget(self.video_info_container)
        self.pages.addWidget(playing_page)

        # Page 2: Settings page
        self.settings_view = SettingsView(self.library, self.engine, self, is_light=self.is_light)
        self.settings_view.theme_mode_changed.connect(self.on_theme_mode_changed)
        self.settings_view.accent_color_changed.connect(self.on_accent_color_changed)
        self.settings_view.audio_profile_changed.connect(self.on_audio_profile_changed)
        self.settings_view.video_aspect_changed.connect(self.on_video_aspect_changed)
        self.pages.addWidget(self.settings_view)

        # Right Up Next / Queue Panel
        self.queue_frame = QFrame(objectName='queue')
        self.queue_frame.setFixedWidth(250)
        self.queue_frame.setMouseTracking(True)
        q = QVBoxLayout(self.queue_frame)
        q.setContentsMargins(18, 18, 18, 16)
        q.addWidget(label('Play queue', 'section'))
        self.queue_count = label('Make room for a good session.', 'muted', True)
        q.addWidget(self.queue_count)
        q.addSpacing(10)

        self.queue_list = QListWidget()
        self.queue_list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.queue_list.setTextElideMode(Qt.TextElideMode.ElideRight)
        self.queue_list.setIconSize(QSize(32, 32))
        self.queue_list.itemDoubleClicked.connect(self.queue_play)
        self.queue_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.queue_list.customContextMenuRequested.connect(self.queue_menu)
        q.addWidget(self.queue_list, 1)

        q.addSpacing(10)
        q.addWidget(label('Extras', 'eyebrow'))
        self.q_bm = button('Bookmark this moment', self.add_bookmark, 'chip')
        self.q_bm.setIcon(get_icon('bookmark', muted_icon, 14))
        q.addWidget(self.q_bm)

        self.loop_button = button('Set loop start · A', self.loop, 'chip')
        q.addWidget(self.loop_button)

        self.q_tools = button('Player tools ↗', self.tools_menu, 'chip')
        self.q_tools.setIcon(get_icon('more', muted_icon, 14))
        q.addWidget(self.q_tools)
        self.content_layout.addWidget(self.queue_frame)

        # Bottom Transport Bar (Windows 11 Media Player Playback Bar)
        self.transport = QFrame(objectName='transport')
        self.transport.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent, True)
        self.transport.setMouseTracking(True)
        controls = QVBoxLayout(self.transport)
        controls.setContentsMargins(20, 10, 20, 12)
        controls.setSpacing(6)

        # Integrated Top Seekbar
        timeline = QHBoxLayout()
        timeline.setSpacing(12)
        self.elapsed = label('0:00', 'muted')
        self.duration = label('0:00', 'muted')
        self.seek = QSlider(Qt.Orientation.Horizontal)
        self.seek.setRange(0, 10000)
        self.seek.setAccessibleName('Playback position')
        self.seek.sliderReleased.connect(self.seek_released)
        timeline.addWidget(self.elapsed)
        timeline.addWidget(self.seek, 1)
        timeline.addWidget(self.duration)
        controls.addLayout(timeline)

        # Bottom 3-Zone Control Area (Strict Mathematical Centering)
        lower = QGridLayout()
        lower.setContentsMargins(0, 0, 0, 0)
        lower.setSpacing(10)

        # Left Zone: Thumbnail, Track Info & Favorite Heart Button (Audio mode)
        self.left_zone_widget = QWidget()
        self.left_zone_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        left_box = QHBoxLayout(self.left_zone_widget)
        left_box.setContentsMargins(0, 0, 0, 0)
        left_box.setSpacing(10)

        self.music_track_info = QWidget()
        m_info_box = QHBoxLayout(self.music_track_info)
        m_info_box.setContentsMargins(0, 0, 0, 0)
        m_info_box.setSpacing(10)

        self.media_thumb = MediaThumbnail(is_light=self.is_light, accent=self.palette['accent'])
        m_info_box.addWidget(self.media_thumb)

        track_info = QVBoxLayout()
        track_info.setSpacing(2)
        self.track_title = label('Nothing playing', 'section')
        self.track_title.setMaximumWidth(280)
        self.track_title.setMinimumWidth(160)
        track_info.addWidget(self.track_title)
        self.status = label('Ready · VLC 4 engine', 'muted')
        self.status.setMaximumWidth(280)
        track_info.addWidget(self.status)
        m_info_box.addLayout(track_info)

        self.favorite_btn = button('', self.toggle_current_favorite, 'transport_round', 'Toggle favorite')
        self.favorite_btn.setFixedSize(32, 32)
        m_info_box.addWidget(self.favorite_btn)
        left_box.addWidget(self.music_track_info)

        # Video mode clean time display (e.g. 0:03 / 2:24)
        self.video_time_label = label('0:00 / 0:00', 'section')
        self.video_time_label.setStyleSheet('color: #ffffff; font-size: 13px; font-weight: 600; padding-left: 6px;')
        self.video_time_label.hide()
        left_box.addWidget(self.video_time_label)
        left_box.addStretch(1)

        lower.addWidget(self.left_zone_widget, 0, 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        # Center Zone: Symmetrical Windows 11 Playback Controls (Perfect Center Alignment)
        transport_icon = '#333333' if self.is_light else '#d0d0d0'
        self.center_zone_widget = QWidget()
        center_box = QHBoxLayout(self.center_zone_widget)
        center_box.setContentsMargins(0, 0, 0, 0)
        center_box.setSpacing(8)

        self.shuffle = button('', self.toggle_shuffle_btn, 'transport_round', 'Shuffle queue')
        self.shuffle.setCheckable(True)
        self.shuffle.setFixedSize(34, 34)
        self.shuffle.setIcon(get_icon('shuffle', transport_icon, 18))
        center_box.addWidget(self.shuffle)

        self.prev_btn = button('', lambda: self.advance(-1), 'transport_round', 'Previous track')
        self.prev_btn.setFixedSize(34, 34)
        self.prev_btn.setIcon(get_icon('prev', transport_icon, 18))
        center_box.addWidget(self.prev_btn)

        self.back10_btn = button('', lambda: self.jump(-10000), 'transport_round', 'Back 10 seconds · ←')
        self.back10_btn.setFixedSize(34, 34)
        self.back10_btn.setIcon(get_icon('back10', transport_icon, 18))
        center_box.addWidget(self.back10_btn)

        # Large Circular WinUI 3 Play/Pause Button
        self.play_button = button('', self.toggle_play, 'play', 'Play or pause · Space')
        self.play_button.setFixedSize(46, 46)
        self.play_button.setIcon(get_icon('play', self.palette['text'], 20))
        center_box.addWidget(self.play_button)

        self.fwd10_btn = button('', lambda: self.jump(10000), 'transport_round', 'Forward 10 seconds · →')
        self.fwd10_btn.setFixedSize(34, 34)
        self.fwd10_btn.setIcon(get_icon('fwd10', transport_icon, 18))
        center_box.addWidget(self.fwd10_btn)

        self.next_btn = button('', self.advance, 'transport_round', 'Next track')
        self.next_btn.setFixedSize(34, 34)
        self.next_btn.setIcon(get_icon('next', transport_icon, 18))
        center_box.addWidget(self.next_btn)

        self.repeat = button('', self.toggle_repeat_btn, 'transport_round', 'Repeat queue')
        self.repeat.setCheckable(True)
        self.repeat.setFixedSize(34, 34)
        self.repeat.setIcon(get_icon('repeat', transport_icon, 18))
        center_box.addWidget(self.repeat)

        lower.addWidget(self.center_zone_widget, 0, 1, Qt.AlignmentFlag.AlignCenter)

        # Right Zone: Playback speed, Volume & Tools
        self.right_zone_widget = QWidget()
        self.right_zone_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        right_box = QHBoxLayout(self.right_zone_widget)
        right_box.setContentsMargins(0, 0, 0, 0)
        right_box.setSpacing(10)
        right_box.addStretch(1)

        self.speed = QComboBox()
        self.speed.setAccessibleName('Playback speed')
        self.speed.addItems(['0.5×', '0.75×', '1×', '1.25×', '1.5×', '2×'])
        self.speed.setCurrentIndex(2)
        self.speed.currentTextChanged.connect(self.change_speed)
        right_box.addWidget(self.speed)

        self.mute = button('', self.toggle_mute, 'transport_round', 'Mute or unmute · M')
        self.mute.setFixedSize(32, 32)
        self.mute.setIcon(get_icon('volume', transport_icon, 18))
        right_box.addWidget(self.mute)

        self.volume = QSlider(Qt.Orientation.Horizontal)
        self.volume.setFixedWidth(90)
        self.volume.setRange(0, 100)
        self.volume.setValue(int(self.library.settings.get('volume', 70)))
        self.volume.setAccessibleName('Volume')
        self.volume.valueChanged.connect(self.change_volume)
        right_box.addWidget(self.volume)

        # Video Mode Tools (Subtitles, Snapshot, Bookmark)
        self.t_sub_btn = button('', self.load_subtitles, 'transport_round', 'Load subtitles (.srt, .vtt)')
        self.t_sub_btn.setFixedSize(32, 32)
        self.t_sub_btn.setIcon(get_icon('subtitles', transport_icon, 16))
        self.t_sub_btn.hide()
        right_box.addWidget(self.t_sub_btn)

        self.t_snap_btn = button('', self.snapshot, 'transport_round', 'Take video screenshot')
        self.t_snap_btn.setFixedSize(32, 32)
        self.t_snap_btn.setIcon(get_icon('camera', transport_icon, 16))
        self.t_snap_btn.hide()
        right_box.addWidget(self.t_snap_btn)

        self.t_bm_btn = button('', self.add_bookmark, 'transport_round', 'Bookmark this moment · B')
        self.t_bm_btn.setFixedSize(32, 32)
        self.t_bm_btn.setIcon(get_icon('bookmark', transport_icon, 16))
        self.t_bm_btn.hide()
        right_box.addWidget(self.t_bm_btn)

        self.fs_btn = button('', self.fullscreen, 'transport_round', 'Toggle full screen · F11')
        self.fs_btn.setFixedSize(32, 32)
        self.fs_btn.setIcon(get_icon('fullscreen', transport_icon, 18))
        right_box.addWidget(self.fs_btn)

        self.more_btn = button('', self.tools_menu, 'transport_round', 'More options')
        self.more_btn.setFixedSize(32, 32)
        self.more_btn.setIcon(get_icon('more', transport_icon, 18))
        right_box.addWidget(self.more_btn)

        lower.addWidget(self.right_zone_widget, 0, 2, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        lower.setColumnStretch(0, 1)
        lower.setColumnStretch(1, 0)
        lower.setColumnStretch(2, 1)

        controls.addLayout(lower)
        self.outer_layout.addWidget(self.transport)

        # Video Watch & Fullscreen Overlays
        self.left_drawer = QFrame(self, objectName='left_drawer')
        self.left_drawer.setAttribute(Qt.WidgetAttribute.WA_NativeWindow)
        self.left_drawer.setMouseTracking(True)
        self.left_drawer_layout = QVBoxLayout(self.left_drawer)
        self.left_drawer_layout.setContentsMargins(0, 0, 0, 0)
        self.left_drawer_layout.setSpacing(0)
        self.left_drawer.setGeometry(-230, 0, 230, self.height())
        self.left_drawer.hide()

        self.right_drawer = QFrame(self, objectName='right_drawer')
        self.right_drawer.setAttribute(Qt.WidgetAttribute.WA_NativeWindow)
        self.right_drawer.setMouseTracking(True)
        self.right_drawer_layout = QVBoxLayout(self.right_drawer)
        self.right_drawer_layout.setContentsMargins(0, 0, 0, 0)
        self.right_drawer_layout.setSpacing(0)
        self.right_drawer.setGeometry(self.width(), 0, 270, self.height())
        self.right_drawer.hide()

        self.video_top_bar = QFrame(self, objectName='video_top_bar')
        self.video_top_bar.setAttribute(Qt.WidgetAttribute.WA_NativeWindow)
        self.video_top_bar.setMouseTracking(True)
        top_bar_box = QHBoxLayout(self.video_top_bar)
        top_bar_box.setContentsMargins(16, 8, 16, 8)
        top_bar_box.setSpacing(12)

        primary_icon = '#1b1b1b' if self.is_light else '#ffffff'
        cap_color = '#333333' if self.is_light else '#cccccc'
        overlay_title_color = '#111111' if self.is_light else '#ffffff'

        self.back_btn = button('Back to library', self.exit_video_to_library, 'chip', 'Back to media collection · Esc')
        self.back_btn.setIcon(get_icon('arrow_left', primary_icon, 14))
        top_bar_box.addWidget(self.back_btn)

        self.video_overlay_title = label('Ocal Media Player', 'section')
        self.video_overlay_title.setStyleSheet(f'font-weight: 600; font-size: 13px; color: {overlay_title_color};')
        top_bar_box.addWidget(self.video_overlay_title)

        top_bar_box.addStretch(1)

        self.v_sub = button('Subtitles', self.load_subtitles, 'chip', 'Load external subtitles (.srt, .vtt)')
        self.v_sub.setIcon(get_icon('subtitles', cap_color, 14))
        top_bar_box.addWidget(self.v_sub)

        self.v_snap = button('Snapshot', self.snapshot, 'chip', 'Take video screenshot')
        self.v_snap.setIcon(get_icon('camera', cap_color, 14))
        top_bar_box.addWidget(self.v_snap)

        self.v_bm = button('Bookmark', self.add_bookmark, 'chip', 'Bookmark this moment')
        self.v_bm.setIcon(get_icon('bookmark', cap_color, 14))
        top_bar_box.addWidget(self.v_bm)

        self.v_fs_btn = button('', self.fullscreen, 'caption_btn', 'Toggle full screen · F11')
        self.v_fs_btn.setIcon(get_icon('fullscreen', cap_color, 14))
        top_bar_box.addWidget(self.v_fs_btn)

        self.v_min_btn = button('', self.showMinimized, 'caption_btn', 'Minimize')
        self.v_min_btn.setIcon(get_icon('cap_min', cap_color, 12))
        top_bar_box.addWidget(self.v_min_btn)

        self.v_max_btn = button('', self.toggle_max, 'caption_btn', 'Maximize')
        self.v_max_btn.setIcon(get_icon('cap_max', cap_color, 12))
        top_bar_box.addWidget(self.v_max_btn)

        self.v_close_btn = button('', self.close, 'caption_close', 'Close')
        self.v_close_btn.setIcon(get_icon('cap_close', cap_color, 12))
        top_bar_box.addWidget(self.v_close_btn)

        self.video_top_bar.setGeometry(0, 0, self.width(), 52)
        self.video_top_bar.hide()

        self.left_anim = QPropertyAnimation(self.left_drawer, b"geometry")
        self.left_anim.setDuration(180)
        self.left_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        self.right_anim = QPropertyAnimation(self.right_drawer, b"geometry")
        self.right_anim.setDuration(180)
        self.right_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    def bind_shortcuts(self):
        def on_escape():
            if self.isFullScreen():
                self.fullscreen()
            elif self.is_video_mode:
                self.exit_video_to_library()

        for key, fn in [('Ctrl+O', self.open_files), ('Ctrl+F', self.search.setFocus),
                        ('F11', self.fullscreen), ('Escape', on_escape),
                        ('Space', self.toggle_play), ('Left', lambda: self.jump(-10000)),
                        ('Right', lambda: self.jump(10000)), ('M', self.toggle_mute),
                        ('B', self.add_bookmark)]:
            shortcut = QShortcut(QKeySequence(key), self)
            def invoke(action=fn, sequence=key):
                if sequence in {'Space', 'Left', 'Right', 'M', 'B'} and isinstance(QApplication.focusWidget(), QLineEdit):
                    return
                action()
            shortcut.activated.connect(invoke)

    def navigate(self, title):
        self.view = title
        self.filter_kind = 'All'
        if title == 'Now playing':
            self.pages.setCurrentIndex(1)
            if self.current and self.current.get('kind') == 'Music':
                self.exit_video_watch_mode()
                self.update_music_stage()
            else:
                self.enter_video_watch_mode()
        elif title == 'Settings':
            self.exit_video_watch_mode()
            self.pages.setCurrentIndex(2)
        else:
            self.exit_video_watch_mode()
            self.pages.setCurrentIndex(0)
        self.heading.setText('Home' if title == 'All media' else title)
        self.refresh()

    def update_music_stage(self):
        if not hasattr(self, 'music_stage'):
            return
        if self.current and self.current.get('kind') == 'Music':
            self.video.hide()
            self.video_info_container.hide()
            self.music_stage.show()
            art = get_media_artwork(self.current['path'], 'Music', 220, 12, is_light=self.is_light, accent=self.palette['accent'])
            self.music_now_art.setPixmap(art)
            self.music_now_title.setText(self.current.get('title', 'Unknown Track'))
            self.music_now_artist.setText(self.current.get('artist') or self.current.get('album') or 'Unknown Artist')
        else:
            self.music_stage.hide()
            self.video.show()
            self.video_info_container.show()

    def enter_video_watch_mode(self):
        if self.is_video_mode:
            return
        self.is_video_mode = True

        # Move sidebar to left drawer
        self.body_layout.removeWidget(self.sidebar)
        self.sidebar.setParent(self.left_drawer)
        self.left_drawer_layout.addWidget(self.sidebar)
        self.sidebar.show()

        # Move queue to right drawer
        self.content_layout.removeWidget(self.queue_frame)
        self.queue_frame.setParent(self.right_drawer)
        self.right_drawer_layout.addWidget(self.queue_frame)
        self.queue_frame.show()

        # Move transport to floating overlay on self
        self.outer_layout.removeWidget(self.transport)
        self.transport.setParent(self)
        self.transport.setProperty('floating', True)
        self.transport.style().unpolish(self.transport)
        self.transport.style().polish(self.transport)

        # Switch transport controls to video mode: hide audio-only widgets, show video tools
        if hasattr(self, 'music_track_info'):
            self.music_track_info.hide()
        if hasattr(self, 'shuffle'):
            self.shuffle.hide()
        if hasattr(self, 'repeat'):
            self.repeat.hide()
        if hasattr(self, 'elapsed'):
            self.elapsed.hide()
        if hasattr(self, 'duration'):
            self.duration.hide()
        if hasattr(self, 'video_time_label'):
            self.video_time_label.show()
        if hasattr(self, 't_sub_btn'):
            self.t_sub_btn.show()
        if hasattr(self, 't_snap_btn'):
            self.t_snap_btn.show()
        if hasattr(self, 't_bm_btn'):
            self.t_bm_btn.show()

        # Hide docked top bar & inner video info bar to make video 100% full view
        self.top_bar_widget.hide()
        self.video_info_container.hide()
        if hasattr(self, 'music_stage'):
            self.music_stage.hide()
        self.video.show()
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Sync titles & show overlay elements
        self.video_overlay_title.setText(self.current['title'] if self.current else 'Ocal Media Player')
        self.left_drawer_open = False
        self.right_drawer_open = False
        self.reposition_video_overlays()
        self.video_top_bar.show()
        self.transport.show()
        self.wake_overlay_controls()

    def exit_video_watch_mode(self):
        if not self.is_video_mode:
            return
        self.is_video_mode = False
        self.overlay_idle_timer.stop()
        self.unsetCursor()

        # Hide overlays
        self.video_top_bar.hide()
        self.left_drawer.hide()
        self.right_drawer.hide()
        self.left_drawer_open = False
        self.right_drawer_open = False

        # Restore sidebar to docked layout
        self.left_drawer_layout.removeWidget(self.sidebar)
        self.sidebar.setParent(self.canvas)
        self.body_layout.insertWidget(0, self.sidebar)
        self.sidebar.show()

        # Restore queue to docked layout
        self.right_drawer_layout.removeWidget(self.queue_frame)
        self.queue_frame.setParent(self.canvas)
        self.content_layout.addWidget(self.queue_frame)
        self.queue_frame.show()

        # Switch transport controls back to audio mode
        if hasattr(self, 'music_track_info'):
            self.music_track_info.show()
        if hasattr(self, 'shuffle'):
            self.shuffle.show()
        if hasattr(self, 'repeat'):
            self.repeat.show()
        if hasattr(self, 'elapsed'):
            self.elapsed.show()
        if hasattr(self, 'duration'):
            self.duration.show()
        if hasattr(self, 'video_time_label'):
            self.video_time_label.hide()
        if hasattr(self, 't_sub_btn'):
            self.t_sub_btn.hide()
        if hasattr(self, 't_snap_btn'):
            self.t_snap_btn.hide()
        if hasattr(self, 't_bm_btn'):
            self.t_bm_btn.hide()

        # Restore transport to docked bottom
        self.transport.setParent(self.canvas)
        self.transport.setProperty('floating', False)
        self.transport.style().unpolish(self.transport)
        self.transport.style().polish(self.transport)
        self.outer_layout.addWidget(self.transport)
        self.transport.show()

        # Restore docked top bar & layout margins
        self.top_bar_widget.show()
        self.video_info_container.show()
        self.main_layout.setContentsMargins(28, 16, 16, 14)

    def exit_video_to_library(self):
        if self.isFullScreen():
            self.showNormal()
        target = 'Videos' if (self.current and self.current.get('kind') == 'Video') else 'All media'
        self.navigate(target)

    def open_left_drawer(self):
        if not self.left_drawer_open:
            self.left_drawer_open = True
            self.left_drawer.show()
            self.left_drawer.raise_()
            self.left_anim.stop()
            self.left_anim.setStartValue(self.left_drawer.geometry())
            self.left_anim.setEndValue(QRect(0, 0, 230, self.height()))
            self.left_anim.start()

    def close_left_drawer(self):
        if self.left_drawer_open:
            self.left_drawer_open = False
            self.left_anim.stop()
            self.left_anim.setStartValue(self.left_drawer.geometry())
            self.left_anim.setEndValue(QRect(-230, 0, 230, self.height()))
            self.left_anim.start()

    def open_right_drawer(self):
        if not self.right_drawer_open:
            self.right_drawer_open = True
            self.right_drawer.show()
            self.right_drawer.raise_()
            self.right_anim.stop()
            self.right_anim.setStartValue(self.right_drawer.geometry())
            self.right_anim.setEndValue(QRect(self.width() - 270, 0, 270, self.height()))
            self.right_anim.start()

    def close_right_drawer(self):
        if self.right_drawer_open:
            self.right_drawer_open = False
            self.right_anim.stop()
            self.right_anim.setStartValue(self.right_drawer.geometry())
            self.right_anim.setEndValue(QRect(self.width(), 0, 270, self.height()))
            self.right_anim.start()

    def reposition_video_overlays(self):
        w = self.width()
        h = self.height()

        top_h = 52
        self.video_top_bar.setGeometry(0, 0, w, top_h)

        trans_h = 86
        self.transport.setGeometry(0, h - trans_h, w, trans_h)

        drawer_w = 230
        left_x = 0 if self.left_drawer_open else -drawer_w
        self.left_drawer.setGeometry(left_x, 0, drawer_w, h)

        queue_w = 270
        right_x = (w - queue_w) if self.right_drawer_open else w
        self.right_drawer.setGeometry(right_x, 0, queue_w, h)

        if self.video_top_bar.isVisible():
            self.video_top_bar.raise_()
        if self.transport.isVisible():
            self.transport.raise_()
        if self.left_drawer_open:
            self.left_drawer.raise_()
        if self.right_drawer_open:
            self.right_drawer.raise_()

    def wake_overlay_controls(self):
        self.unsetCursor()
        if self.is_video_mode:
            if not self.video_top_bar.isVisible():
                self.video_top_bar.show()
                self.video_top_bar.raise_()
            if not self.transport.isVisible():
                self.transport.show()
                self.transport.raise_()
            if self.left_drawer_open:
                self.left_drawer.raise_()
            if self.right_drawer_open:
                self.right_drawer.raise_()
            self.overlay_idle_timer.start(2500)

    def on_overlay_idle_timeout(self):
        if not self.is_video_mode:
            return
        if self.engine and self.engine.state == 2:  # Playing
            if self.left_drawer_open or self.right_drawer_open:
                return
            pos = self.mapFromGlobal(QCursor.pos())
            if self.transport.geometry().contains(pos) or self.video_top_bar.geometry().contains(pos):
                self.overlay_idle_timer.start(1000)
                return
            self.video_top_bar.hide()
            self.transport.hide()
            self.setCursor(Qt.CursorShape.BlankCursor)

    def handle_video_mouse_move(self, event):
        if not self.is_video_mode:
            return

        pos = self.mapFromGlobal(QCursor.pos())
        x = pos.x()
        y = pos.y()
        w = self.width()
        h = self.height()

        self.wake_overlay_controls()

        # Edge hover detection:
        # Sharp Left edge: x <= 20
        if x <= 20 and 0 <= y <= h:
            self.open_left_drawer()
        elif self.left_drawer_open:
            if x > self.left_drawer.width() + 30:
                self.close_left_drawer()

        # Sharp Right edge: x >= w - 20
        if x >= w - 20 and 0 <= y <= h:
            self.open_right_drawer()
        elif self.right_drawer_open:
            if x < w - self.right_drawer.width() - 30:
                self.close_right_drawer()

    def set_filter(self, kind):
        self.filter_kind = kind
        self.refresh()

    def set_collection_view(self, mode):
        self.collection_layout_mode = mode
        accent_text = self.palette.get('text', '#ffffff') if hasattr(self, 'palette') else WIN11_ACCENT_TEXT
        muted_icon = '#666666' if getattr(self, 'is_light', False) else '#a0a0a0'
        if mode == 'grid':
            self.collection_stack.setCurrentIndex(1)
            self.btn_view_grid.setChecked(True)
            self.btn_view_list.setChecked(False)
            self.btn_view_grid.setIcon(get_icon('view_grid', accent_text, 16))
            self.btn_view_list.setIcon(get_icon('view_list', muted_icon, 16))
        else:
            self.collection_stack.setCurrentIndex(0)
            self.btn_view_list.setChecked(True)
            self.btn_view_grid.setChecked(False)
            self.btn_view_list.setIcon(get_icon('view_list', accent_text, 16))
            self.btn_view_grid.setIcon(get_icon('view_grid', muted_icon, 16))

    def refresh(self):
        for title, b in self.nav.items():
            b.setChecked(title == self.view)
        is_settings = (self.view == 'Settings')
        self.search.setVisible(not is_settings)
        self.open_btn.setVisible(not is_settings)
        self.folder_button.setVisible(not is_settings)
        self.scan_btn.setVisible(not is_settings)
        self.stream_btn.setVisible(not is_settings)
        if is_settings:
            return
        for chip in self.chips:
            chip.setChecked(chip.text() == self.filter_kind)
        query = self.search.text().casefold()
        items = [x for x in self.library.items if query in x['title'].casefold()]
        if self.view == 'Music':
            items = [x for x in items if x['kind'] == 'Music']
        elif self.view == 'Videos':
            items = [x for x in items if x['kind'] == 'Video']
        elif self.view == 'Favorites':
            items = [x for x in items if x['favorite']]
        elif self.view == 'Recently played':
            items = sorted([x for x in items if x['played']], key=lambda x: x['played'], reverse=True)
        if self.filter_kind != 'All':
            items = [x for x in items if x['kind'] == self.filter_kind]
        self.visible_items = items

        # Populate List View (Table)
        self.table.setRowCount(len(items))
        target_path = self.current.get('path', '').casefold() if self.current else ''
        for row, entry in enumerate(items):
            title = entry['title']
            if entry['position'] > 5000:
                title += '   ·   Resume ' + clock(entry['position'])
            kind = entry['kind']
            is_playing = bool(target_path and entry.get('path', '').casefold() == target_path)
            
            # 0: Title column with real artwork thumbnail
            title_cell = QTableWidgetItem(title)
            title_cell.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            title_cell.setToolTip(entry['path'])
            art_thumb = get_media_artwork(entry['path'], kind, 36, 4, is_light=self.is_light, accent=self.palette['accent'])
            title_cell.setIcon(QIcon(art_thumb))
            if is_playing:
                title_cell.setForeground(QColor(self.palette['accent']))
                font = title_cell.font()
                font.setBold(True)
                title_cell.setFont(font)
            self.table.setItem(row, 0, title_cell)

            # 1: Artist / Extra column
            artist_text = entry.get('artist') or ('—' if kind == 'Music' else kind)
            artist_cell = QTableWidgetItem(artist_text)
            artist_cell.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            artist_cell.setToolTip(artist_text)
            if is_playing:
                artist_cell.setForeground(QColor(self.palette['accent']))
            self.table.setItem(row, 1, artist_cell)

            # 2: Kind / Type column
            kind_cell = QTableWidgetItem(kind)
            kind_cell.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            kind_cell.setToolTip(kind)
            self.table.setItem(row, 2, kind_cell)

            # 3: Length column (Right-aligned, clock format)
            duration_text = clock(entry['duration']) if entry['duration'] else '—'
            dur_cell = QTableWidgetItem(duration_text)
            dur_cell.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            dur_cell.setToolTip(duration_text)
            self.table.setItem(row, 3, dur_cell)

            # 4: Saved / Favorite column with interactive heart
            fav_cell = QTableWidgetItem()
            fav_cell.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if entry.get('favorite'):
                fav_cell.setIcon(get_icon('heart_fill', self.palette['accent'], 16))
                fav_cell.setToolTip('In favorites (click to remove)')
            else:
                fav_icon_color = 'rgba(0, 0, 0, 0.25)' if self.is_light else 'rgba(255, 255, 255, 0.22)'
                fav_cell.setIcon(get_icon('heart_outline', fav_icon_color, 15))
                fav_cell.setToolTip('Click to add to favorites')
            self.table.setItem(row, 4, fav_cell)

        # Populate Grid View (Cards with 140x140 artwork)
        self.grid_view.clear()
        for idx, entry in enumerate(items):
            kind = entry['kind']
            dur_str = clock(entry['duration']) if entry.get('duration') else ''
            subtitle = entry.get('artist') or kind
            sub_text = f"{subtitle}  ·  {dur_str}" if dur_str else subtitle
            disp_title = entry['title']
            if len(disp_title) > 34:
                disp_title = disp_title[:31] + '...'
            card_label = f"{disp_title}\n{sub_text}"
            item = QListWidgetItem(card_label)
            item.setToolTip(f"{entry['title']}\n{entry['path']}")
            art = get_media_artwork(entry['path'], kind, 140, 8, is_light=self.is_light, accent=self.palette['accent'])
            item.setIcon(QIcon(art))
            item.setData(Qt.ItemDataRole.UserRole, idx)
            self.grid_view.addItem(item)

        # Informative count label
        if self.view == 'All media':
            m_count = sum(1 for x in items if x['kind'] == 'Music')
            v_count = sum(1 for x in items if x['kind'] == 'Video')
            self.count.setText(f'{len(items)} items ({m_count} music, {v_count} videos)')
        elif self.view == 'Music':
            self.count.setText(f'{len(items)} music tracks')
        elif self.view == 'Videos':
            self.count.setText(f'{len(items)} videos')
        elif self.view == 'Favorites':
            self.count.setText(f'{len(items)} favorites')
        else:
            self.count.setText(f'{len(items)} items')

        self.empty.setVisible(not items)
        self.empty.setText('No matching media. Try another search or filter.' if self.library.items else 'Your next favorite belongs here.\nOpen files, add folders, or click Scan PC to start.')
        self.update_active_selection()
        self.update_favorite_button()

    def save(self):
        try:
            self.library.save()
        except OSError as exc:
            self.status.setText(f'Could not save library: {exc}')

    def import_paths(self, paths):
        try:
            added = self.library.add(paths)
            self.status.setText(f'{len(added)} media files ready in your library.')
            self.refresh()
            return added
        except OSError as exc:
            self.status.setText(f'Import failed: {exc}')
            return []

    def open_files(self):
        paths, _ = QFileDialog.getOpenFileNames(
            self, 'Add media', '',
            'Media files (' + ' '.join('*' + e for e in sorted(AUDIO | VIDEO)) + ');;Audio files (' + ' '.join('*' + e for e in sorted(AUDIO)) + ');;Video files (' + ' '.join('*' + e for e in sorted(VIDEO)) + ');;All files (*)'
        )
        if paths:
            added = self.import_paths(paths)
            if added:
                self.start_queue(added)

    def open_folder(self):
        directory = QFileDialog.getExistingDirectory(self, 'Add media folder')
        if directory:
            watch = self.library.settings.setdefault('watch_folders', [])
            if directory not in watch:
                watch.append(directory)
                self.save()
            self.scan_folder(directory)

    def scan_folder(self, directory):
        if self.scanner and self.scanner.isRunning():
            self.status.setText('A folder import is already running.')
            return
        self.folder_button.setEnabled(False)
        self.status.setText('Looking for media in your folder…')
        self.scanner = FolderScan(directory)
        self.scanner.found.connect(self.import_paths)
        self.scanner.failed.connect(lambda message: self.status.setText('Folder import failed: ' + message))
        self.scanner.finished.connect(lambda: self.folder_button.setEnabled(True))
        self.scanner.start()

    def open_stream(self):
        url, ok = FluentDialog.prompt_stream(self)
        if ok and url.strip():
            added = self.import_paths([url.strip()])
            if added:
                self.start_queue(added)
            else:
                self.status.setText('Enter a supported network URL, including its protocol.')

    def start_queue(self, items, index=0):
        self.queue = list(items)
        self.queue_index = index
        self.update_queue()
        if self.queue:
            self.play_item(self.queue[index])

    def table_play(self, row, column=0):
        if column == 4:
            return
        self.start_queue(self.visible_items, row)

    def table_cell_clicked(self, row, column):
        if column == 4:
            if 0 <= row < len(self.visible_items):
                self.favorite(self.visible_items[row])

    def grid_play(self, item):
        idx = item.data(Qt.ItemDataRole.UserRole)
        if idx is not None and 0 <= idx < len(self.visible_items):
            self.start_queue(self.visible_items, idx)

    def play_item(self, entry):
        if '://' not in entry['path'] and not Path(entry['path']).is_file():
            self.status.setText('File not found. Re-add it from its new location.')
            return
        self.store_position()
        try:
            self.engine.play(entry['path'])
        except RuntimeError as exc:
            self.status.setText(str(exc))
            return
        self.current = entry
        self.has_played = False
        self.pending_resume = entry['position'] if entry['duration'] - entry['position'] > 3000 else 0
        entry['played'] = time.time()
        self.a = self.b = None
        self.loop_button.setText('Set loop start · A')
        self.track_title.setText(entry['title'])
        self.track_title.setToolTip(entry['title'])
        art = get_media_artwork(entry['path'], entry.get('kind', 'Music'), 42, 6, is_light=self.is_light, accent=self.palette['accent'])
        self.media_thumb.set_media(entry.get('kind', ''), art)
        self.update_favorite_button()
        self.playing_title.setText(entry['title'])
        if hasattr(self, 'video_overlay_title'):
            self.video_overlay_title.setText(entry['title'])
            self.video_overlay_title.setToolTip(entry['title'])
        self.status.setText('Opening ' + entry['title'])
        self.engine.volume(self.volume.value())
        if entry['kind'] in {'Video', 'Stream'}:
            self.navigate('Now playing')
        else:
            if self.view == 'Now playing':
                self.exit_video_watch_mode()
                self.update_music_stage()
            self.refresh()
        self.update_queue()
        self.update_active_selection()
        self.save()

    def update_active_selection(self):
        if not self.current:
            self.table.clearSelection()
            self.grid_view.clearSelection()
            return

        target_path = self.current.get('path', '').casefold()
        active_row = -1
        for i, item in enumerate(self.visible_items):
            if item.get('path', '').casefold() == target_path:
                active_row = i
                break

        if active_row >= 0:
            self.table.selectRow(active_row)
            item = self.table.item(active_row, 0)
            if item:
                self.table.scrollToItem(item, QAbstractItemView.ScrollHint.EnsureVisible)
            self.grid_view.setCurrentRow(active_row)
            g_item = self.grid_view.item(active_row)
            if g_item:
                self.grid_view.scrollToItem(g_item, QAbstractItemView.ScrollHint.EnsureVisible)
        else:
            self.table.clearSelection()
            self.grid_view.clearSelection()

    def store_position(self):
        if self.current and self.engine and self.has_played and self.engine.media_ready:
            self.current['position'] = self.engine.time
            if self.engine.length > 0:
                self.current['duration'] = self.engine.length
            self.save()

    def toggle_play(self):
        if not self.current:
            if self.visible_items:
                self.start_queue(self.visible_items)
            else:
                self.open_files()
        elif self.engine.state in (4, 6):
            self.play_item(self.current)
        else:
            self.engine.pause(self.engine.state == 2)

    def advance(self, step=1):
        if not self.queue:
            return
        if isinstance(step, bool):
            step = 1
        index = self.queue_index + step
        if self.shuffle.isChecked() and len(self.queue) > 1:
            index = random.choice([i for i in range(len(self.queue)) if i != self.queue_index])
        elif not 0 <= index < len(self.queue):
            if not self.repeat.isChecked():
                return
            index %= len(self.queue)
        self.queue_index = index
        self.play_item(self.queue[index])

    def toggle_shuffle_btn(self):
        accent = self.palette['accent'] if hasattr(self, 'palette') else WIN11_ACCENT
        transport_icon = '#333333' if getattr(self, 'is_light', False) else '#d0d0d0'
        self.shuffle.setIcon(get_icon('shuffle', accent if self.shuffle.isChecked() else transport_icon, 18))

    def toggle_repeat_btn(self):
        accent = self.palette['accent'] if hasattr(self, 'palette') else WIN11_ACCENT
        transport_icon = '#333333' if getattr(self, 'is_light', False) else '#d0d0d0'
        self.repeat.setIcon(get_icon('repeat', accent if self.repeat.isChecked() else transport_icon, 18))

    def update_queue(self):
        self.queue_list.clear()
        for i, entry in enumerate(self.queue):
            item = QListWidgetItem(f'{i + 1:02}   {entry["title"]}\n       {entry["kind"]}')
            item.setToolTip(entry['path'])
            art = get_media_artwork(entry['path'], entry.get('kind', 'Music'), 32, 4, is_light=self.is_light, accent=self.palette['accent'])
            item.setIcon(QIcon(art))
            self.queue_list.addItem(item)
        self.queue_list.setCurrentRow(self.queue_index)
        self.queue_count.setText(f'{len(self.queue)} tracks in this session' if self.queue else 'Double-click a file to start a session.')

    def queue_play(self, item):
        self.queue_index = self.queue_list.row(item)
        self.play_item(self.queue[self.queue_index])

    def library_menu(self, pos):
        row = self.table.rowAt(pos.y())
        if row < 0 or row >= len(self.visible_items):
            return
        self.show_entry_context_menu(self.visible_items[row], row, self.table.viewport().mapToGlobal(pos))

    def grid_menu(self, pos):
        item = self.grid_view.itemAt(pos)
        if not item:
            return
        idx = item.data(Qt.ItemDataRole.UserRole)
        if idx is not None and 0 <= idx < len(self.visible_items):
            self.show_entry_context_menu(self.visible_items[idx], idx, self.grid_view.viewport().mapToGlobal(pos))

    def show_entry_context_menu(self, entry, index, global_pos):
        menu = QMenu(self)
        menu.addAction('Play', lambda: self.start_queue(self.visible_items, index))
        menu.addAction('Add to queue', lambda: self.enqueue(entry))
        menu.addAction('Remove favorite' if entry['favorite'] else 'Add to favorites', lambda: self.favorite(entry))
        bookmarks = menu.addMenu('Jump to bookmark')
        bookmarks.setEnabled(bool(entry['bookmarks']))
        for mark in entry['bookmarks']:
            bookmarks.addAction(f'{clock(mark["time"])} · {mark["name"]}', lambda m=mark: self.jump_bookmark(entry, m['time']))
        menu.addSeparator()
        menu.addAction('Remove from library (keep file)', lambda: self.remove_item(entry))
        menu.exec(global_pos)

    def enqueue(self, entry):
        self.queue.append(entry)
        self.update_queue()

    def favorite(self, entry):
        entry['favorite'] = not entry['favorite']
        self.save()
        self.refresh()
        self.update_favorite_button()

    def toggle_current_favorite(self):
        if self.current:
            self.favorite(self.current)

    def update_favorite_button(self):
        if hasattr(self, 'favorite_btn'):
            is_fav = bool(self.current and self.current.get('favorite'))
            icon_name = 'heart_fill' if is_fav else 'heart_outline'
            accent = self.palette['accent'] if hasattr(self, 'palette') else WIN11_ACCENT
            unfav_color = '#616161' if getattr(self, 'is_light', False) else '#8d8d8d'
            icon_color = accent if is_fav else unfav_color
            self.favorite_btn.setIcon(get_icon(icon_name, icon_color, 18))

    def remove_item(self, entry):
        self.library.items.remove(entry)
        self.save()
        self.refresh()

    def queue_menu(self, pos):
        row = self.queue_list.indexAt(pos).row()
        if row < 0:
            return
        menu = QMenu(self)
        if row != self.queue_index:
            menu.addAction('Remove from queue', lambda: self.remove_queue(row))
        if row > 0:
            menu.addAction('Move up', lambda: self.move_queue(row, row - 1))
        if row < len(self.queue) - 1:
            menu.addAction('Move down', lambda: self.move_queue(row, row + 1))
        menu.exec(self.queue_list.viewport().mapToGlobal(pos))

    def remove_queue(self, row):
        self.queue.pop(row)
        if row < self.queue_index:
            self.queue_index -= 1
        self.update_queue()

    def move_queue(self, row, target):
        self.queue[row], self.queue[target] = self.queue[target], self.queue[row]
        if self.queue_index == row:
            self.queue_index = target
        elif self.queue_index == target:
            self.queue_index = row
        self.update_queue()

    def seek_released(self):
        if self.engine and self.engine.seekable:
            self.pending_resume = 0
            self.engine.seek(self.engine.length * self.seek.value() / 10000)

    def jump(self, amount):
        if self.current and self.engine.seekable:
            self.engine.seek(min(self.engine.length, max(0, self.engine.time + amount)))

    def change_volume(self, value):
        if self.engine:
            self.engine.volume(value)
        self.library.settings['volume'] = value
        transport_icon = '#333333' if getattr(self, 'is_light', False) else '#d0d0d0'
        self.mute.setIcon(get_icon('mute' if value == 0 else 'volume', transport_icon, 18))

    def toggle_mute(self):
        if self.volume.value():
            self.previous_volume = self.volume.value()
            self.volume.setValue(0)
        else:
            self.volume.setValue(getattr(self, 'previous_volume', 70))

    def change_speed(self, value):
        if self.engine and self.engine.rate(float(value.rstrip('×'))) != 0:
            self.status.setText('This media does not support changing playback speed.')

    def loop(self):
        if not self.current or not self.engine.seekable:
            self.status.setText('Play seekable media before setting a loop.')
        elif self.a is None:
            self.a = self.engine.time
            self.loop_button.setText(f'A: {clock(self.a)} · Set B')
        elif self.b is None:
            if self.engine.time < self.a + 500:
                self.status.setText('Choose an end point at least half a second after A.')
                return
            self.b = self.engine.time
            self.loop_button.setText('Loop active · Clear A–B')
        else:
            self.a = self.b = None
            self.loop_button.setText('Set loop start · A')

    def add_bookmark(self):
        if not self.current or not self.engine.seekable:
            self.status.setText('Play seekable media to bookmark a moment.')
            return
        moment = self.engine.time
        name, ok = QInputDialog.getText(self, 'Save a moment', 'Bookmark name', text='Moment at ' + clock(moment))
        if ok and name.strip():
            self.current['bookmarks'].append({'time': moment, 'name': name.strip()})
            self.save()
            self.status.setText('Bookmark saved. Find it in the media’s right-click menu.')

    def jump_bookmark(self, entry, moment):
        if self.current is entry and self.engine.seekable:
            self.engine.seek(moment)
        else:
            self.start_queue([entry])
            self.pending_resume = moment

    def tools_menu(self):
        menu = QMenu(self)
        menu.addAction('Load subtitles…', self.load_subtitles)
        menu.addAction('Save video snapshot…', self.snapshot)
        timer = menu.addMenu('Sleep timer')
        for minutes in (15, 30, 60, 90):
            timer.addAction(f'{minutes} minutes', lambda m=minutes: self.set_sleep(m))
        timer.addAction('Cancel timer', lambda: self.set_sleep(0))
        pin = menu.addAction('Always on top')
        pin.setCheckable(True)
        pin.setChecked(bool(self.windowFlags() & Qt.WindowType.WindowStaysOnTopHint))
        pin.triggered.connect(self.pin_window)
        menu.exec(self.cursor().pos())

    def set_sleep(self, minutes):
        self.sleep_deadline = time.monotonic() + minutes * 60 if minutes else None
        self.status.setText(f'Playback will pause in {minutes} minutes.' if minutes else 'Sleep timer canceled.')

    def pin_window(self, enabled):
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, enabled)
        self.show()

    def load_subtitles(self):
        if not self.current:
            self.status.setText('Open a video before adding subtitles.')
            return
        path, _ = QFileDialog.getOpenFileName(self, 'Load subtitles', '', 'Subtitles (*.srt *.ass *.ssa *.vtt *.sub)')
        if path:
            self.status.setText('Subtitles loaded.' if self.engine.subtitle(path) == 0 else 'VLC could not load these subtitles.')

    def snapshot(self):
        if not self.current or self.current['kind'] == 'Music':
            self.status.setText('Play a video before saving a snapshot.')
            return
        path, _ = QFileDialog.getSaveFileName(self, 'Save video snapshot', 'snapshot.png', 'PNG image (*.png)')
        if path:
            self.status.setText('Snapshot requested: ' + path if self.engine.snapshot(path) == 0 else 'No video frame available for a snapshot.')

    def tick(self):
        if self.sleep_deadline and time.monotonic() >= self.sleep_deadline:
            self.engine.pause(True)
            self.sleep_deadline = None
            self.status.setText('Sleep timer finished. Playback paused.')
        if not self.current:
            return
        if not self.engine.media_ready:
            return
        state = self.engine.state
        length, position = self.engine.length, self.engine.time
        if state == 2:
            if not self.has_played:
                self.has_played = True
                self.engine.rate(float(self.speed.currentText().rstrip('×')))
                self.status.setText('Playing · ' + self.current['title'])
            if self.pending_resume and self.engine.seekable and length > 0:
                self.engine.seek(min(self.pending_resume, max(0, length - 1000)))
                self.pending_resume = 0
            if self.a is not None and self.b is not None and position >= self.b:
                self.engine.seek(self.a)
        
        # WinUI 3 Play/Pause icon (no emojis or text glyphs)
        self.play_button.setIcon(get_icon('pause' if state == 2 else 'play', self.palette['text'], 20))
        self.elapsed.setText(clock(position))
        self.duration.setText(clock(length))
        if hasattr(self, 'video_time_label'):
            self.video_time_label.setText(f"{clock(position)} / {clock(length)}")
        self.seek.setEnabled(self.engine.seekable)
        if not self.seek.isSliderDown():
            self.seek.setValue(int(position / length * 10000) if length else 0)
        if state == 6:
            self.status.setText('Playback failed. Check the file or stream URL and try again.')
            self.has_played = False
        elif state == 4 and self.has_played:
            self.current['position'] = 0
            self.current['duration'] = max(length, self.current['duration'])
            self.has_played = False
            self.save()
            self.advance()
        elif state in (2, 3) and time.monotonic() - self.last_save > 5:
            self.store_position()
            self.last_save = time.monotonic()

    def fullscreen(self):
        cap_color = '#333333' if getattr(self, 'is_light', False) else '#cccccc'
        if self.isFullScreen():
            self.showNormal()
            if hasattr(self, 'caption_container'):
                self.caption_container.show()
            if hasattr(self, 'v_min_btn'):
                self.v_min_btn.show()
                self.v_max_btn.show()
                self.v_fs_btn.setIcon(get_icon('fullscreen', cap_color, 14))
                self.v_fs_btn.setToolTip('Toggle full screen · F11')
        else:
            if not self.is_video_mode and self.current and self.current.get('kind') in {'Video', 'Stream'}:
                self.enter_video_watch_mode()
            self.showFullScreen()
            if hasattr(self, 'caption_container'):
                self.caption_container.hide()
            if hasattr(self, 'v_min_btn'):
                self.v_min_btn.hide()
                self.v_max_btn.hide()
                self.v_fs_btn.setIcon(get_icon('cap_restore', cap_color, 14))
                self.v_fs_btn.setToolTip('Exit full screen · F11')
        if self.is_video_mode:
            self.reposition_video_overlays()
            self.wake_overlay_controls()
        apply_win11_frameless_attributes(self, getattr(self, 'is_light', False))

    def toggle_max(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()
        self.update_max_button()
        apply_win11_frameless_attributes(self, getattr(self, 'is_light', False))

    def update_max_button(self):
        cap_color = '#333333' if getattr(self, 'is_light', False) else '#cccccc'
        if hasattr(self, 'max_btn'):
            is_max = self.isMaximized()
            self.max_btn.setIcon(get_icon('cap_restore' if is_max else 'cap_max', cap_color, 12))
            self.max_btn.setToolTip('Restore' if is_max else 'Maximize')
        if hasattr(self, 'v_max_btn'):
            is_max = self.isMaximized()
            self.v_max_btn.setIcon(get_icon('cap_restore' if is_max else 'cap_max', cap_color, 12))
            self.v_max_btn.setToolTip('Restore' if is_max else 'Maximize')

    def check_system_theme(self, force=False):
        """Detect live Windows 11 Light/Dark theme mode & Accent color changes or settings overrides."""
        win_is_light, win_palette = refresh_win11_theme()
        user_mode = self.library.settings.get('theme_mode', 'system') if hasattr(self, 'library') else 'system'
        if user_mode == 'dark':
            effective_is_light = False
        elif user_mode == 'light':
            effective_is_light = True
        else:
            effective_is_light = win_is_light

        user_accent = self.library.settings.get('accent_color', 'system') if hasattr(self, 'library') else 'system'
        if user_accent and user_accent.lower() != 'system':
            effective_palette = make_accent_palette(user_accent, effective_is_light)
        else:
            effective_palette = get_windows_accent_palette(effective_is_light)

        if not force and hasattr(self, '_current_is_light') and self._current_is_light == effective_is_light:
            if hasattr(self, '_current_accent') and self._current_accent == effective_palette['accent']:
                return

        self._current_is_light = effective_is_light
        self._current_accent = effective_palette['accent']
        self.is_light = effective_is_light
        self.palette = effective_palette

        # Apply updated stylesheet
        app = QApplication.instance()
        if app:
            app.setStyleSheet(get_stylesheet(effective_palette, effective_is_light))

        # Re-apply Windows 11 DWM attributes
        apply_win11_frameless_attributes(self, effective_is_light)

        # Clear artwork cache so fallback placeholder cards match light/dark mode
        clear_artwork_cache()

        # Update all UI vector icon colors and badges
        self.update_theme_elements()

        # Update settings view if present
        if hasattr(self, 'settings_view'):
            self.settings_view.apply_theme(effective_is_light, effective_palette)

        # Refresh collection view and now playing
        self.refresh()
        if hasattr(self, 'update_queue'):
            self.update_queue()

    def on_theme_mode_changed(self, mode):
        self.check_system_theme(force=True)

    def on_accent_color_changed(self, accent_hex):
        self.check_system_theme(force=True)

    def on_audio_profile_changed(self, profile):
        if self.engine:
            self.engine.set_equalizer_preset(profile)

    def on_video_aspect_changed(self, aspect):
        if self.engine:
            self.engine.set_aspect_ratio(aspect)

    def auto_check_updates(self):
        if hasattr(self, 'settings_view'):
            self.settings_view.check_for_updates()

    def update_theme_elements(self):
        """Update all vector icon colors, brand badge, and accent highlights for current theme."""
        is_light = getattr(self, 'is_light', False)
        palette = getattr(self, 'palette', None) or get_windows_accent_palette(is_light)
        accent = palette['accent']
        accent_text = palette['text']
        accent_base = palette.get('base', accent)

        cap_color = '#333333' if is_light else '#cccccc'
        primary_icon = '#1b1b1b' if is_light else '#ffffff'
        nav_icon = '#444444' if is_light else '#cccccc'
        muted_icon = '#666666' if is_light else '#a0a0a0'
        transport_icon = '#333333' if is_light else '#d0d0d0'

        # 1. Brand icon badge
        if hasattr(self, 'icon_badge'):
            self.icon_badge.setStyleSheet(
                f'background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {accent}, stop:1 {accent_base});'
                'border-radius: 6px;'
            )
            p_pix = QPixmap(26, 26)
            p_pix.fill(Qt.GlobalColor.transparent)
            bp = QPainter(p_pix)
            bp.setRenderHint(QPainter.RenderHint.Antialiasing)
            get_icon('play', accent_text, 16).paint(bp, QRect(5, 5, 16, 16))
            bp.end()
            self.icon_badge.setPixmap(p_pix)

        # 2. Sidebar Navigation
        if hasattr(self, 'nav'):
            for key, b in self.nav.items():
                icon_name = self.nav_icons.get(key, 'music') if hasattr(self, 'nav_icons') else 'music'
                b.setIcon(get_icon(icon_name, nav_icon, 18))
        if hasattr(self, 'settings_btn'):
            self.settings_btn.setIcon(get_icon('settings', nav_icon, 18))
        if hasattr(self, 'shortcuts_btn'):
            self.shortcuts_btn.setIcon(get_icon('keyboard', nav_icon, 18))
        if hasattr(self, 'about_btn'):
            self.about_btn.setIcon(get_icon('info', nav_icon, 18))
        if hasattr(self, 'sidebar_divider'):
            div_bg = 'rgba(0, 0, 0, 0.08)' if is_light else 'rgba(255, 255, 255, 0.08)'
            self.sidebar_divider.setStyleSheet(f'background: {div_bg}; margin: 6px 2px;')

        # 3. Top Header Bar
        if hasattr(self, 'open_btn'):
            self.open_btn.setIcon(get_icon('open_files', accent_text, 16))
        if hasattr(self, 'folder_button'):
            self.folder_button.setIcon(get_icon('folder', primary_icon, 16))
        if hasattr(self, 'scan_btn'):
            self.scan_btn.setIcon(get_icon('refresh', primary_icon, 16))
        if hasattr(self, 'stream_btn'):
            self.stream_btn.setIcon(get_icon('stream', primary_icon, 16))
        if hasattr(self, 'min_btn'):
            self.min_btn.setIcon(get_icon('cap_min', cap_color, 12))
        if hasattr(self, 'close_btn'):
            self.close_btn.setIcon(get_icon('cap_close', cap_color, 12))
        self.update_max_button()

        # 4. View Switchers
        if hasattr(self, 'btn_view_list') and hasattr(self, 'btn_view_grid'):
            is_grid = (getattr(self, 'collection_layout_mode', 'list') == 'grid')
            self.btn_view_grid.setIcon(get_icon('view_grid', accent_text if is_grid else muted_icon, 16))
            self.btn_view_list.setIcon(get_icon('view_list', muted_icon if is_grid else accent_text, 16))

        # 5. Extras & Video Tools
        if hasattr(self, 'q_bm'):
            self.q_bm.setIcon(get_icon('bookmark', muted_icon, 14))
        if hasattr(self, 'q_tools'):
            self.q_tools.setIcon(get_icon('more', muted_icon, 14))
        if hasattr(self, 'sub_btn'):
            self.sub_btn.setIcon(get_icon('subtitles', muted_icon, 16))
        if hasattr(self, 'snap_btn'):
            self.snap_btn.setIcon(get_icon('camera', muted_icon, 16))
        if hasattr(self, 'bm_btn'):
            self.bm_btn.setIcon(get_icon('bookmark', muted_icon, 16))
        if hasattr(self, 'fs_tool'):
            self.fs_tool.setIcon(get_icon('fullscreen', muted_icon, 16))

        # 6. Transport Controls
        if hasattr(self, 'shuffle'):
            self.shuffle.setIcon(get_icon('shuffle', accent if self.shuffle.isChecked() else transport_icon, 18))
        if hasattr(self, 'prev_btn'):
            self.prev_btn.setIcon(get_icon('prev', transport_icon, 18))
        if hasattr(self, 'back10_btn'):
            self.back10_btn.setIcon(get_icon('back10', transport_icon, 18))
        if hasattr(self, 'play_button'):
            is_playing = (self.engine.state == 2) if (self.engine and hasattr(self.engine, 'state')) else False
            self.play_button.setIcon(get_icon('pause' if is_playing else 'play', accent_text, 20))
        if hasattr(self, 'fwd10_btn'):
            self.fwd10_btn.setIcon(get_icon('fwd10', transport_icon, 18))
        if hasattr(self, 'next_btn'):
            self.next_btn.setIcon(get_icon('next', transport_icon, 18))
        if hasattr(self, 'repeat'):
            self.repeat.setIcon(get_icon('repeat', accent if self.repeat.isChecked() else transport_icon, 18))
        if hasattr(self, 'mute'):
            vol = self.volume.value() if hasattr(self, 'volume') else 70
            self.mute.setIcon(get_icon('mute' if vol == 0 else 'volume', transport_icon, 18))
        if hasattr(self, 'fs_btn'):
            self.fs_btn.setIcon(get_icon('fullscreen', transport_icon, 18))
        if hasattr(self, 't_sub_btn'):
            self.t_sub_btn.setIcon(get_icon('subtitles', transport_icon, 16))
        if hasattr(self, 't_snap_btn'):
            self.t_snap_btn.setIcon(get_icon('camera', transport_icon, 16))
        if hasattr(self, 't_bm_btn'):
            self.t_bm_btn.setIcon(get_icon('bookmark', transport_icon, 16))
        if hasattr(self, 'more_btn'):
            self.more_btn.setIcon(get_icon('more', transport_icon, 18))
        if hasattr(self, 'media_thumb'):
            self.media_thumb.set_theme(is_light, accent)
        self.update_favorite_button()

        # 7. Video Overlay Controls
        if hasattr(self, 'video_overlay_title'):
            self.video_overlay_title.setStyleSheet(f"font-weight: 600; font-size: 13px; color: {'#111111' if is_light else '#ffffff'};")
        if hasattr(self, 'back_btn'):
            self.back_btn.setIcon(get_icon('arrow_left', primary_icon, 14))
        if hasattr(self, 'v_sub'):
            self.v_sub.setIcon(get_icon('subtitles', cap_color, 14))
        if hasattr(self, 'v_snap'):
            self.v_snap.setIcon(get_icon('camera', cap_color, 14))
        if hasattr(self, 'v_bm'):
            self.v_bm.setIcon(get_icon('bookmark', cap_color, 14))
        if hasattr(self, 'v_fs_btn'):
            is_fullscreen = self.isFullScreen()
            self.v_fs_btn.setIcon(get_icon('cap_restore' if is_fullscreen else 'fullscreen', cap_color, 14))
        if hasattr(self, 'v_min_btn'):
            self.v_min_btn.setIcon(get_icon('cap_min', cap_color, 12))
        if hasattr(self, 'v_close_btn'):
            self.v_close_btn.setIcon(get_icon('cap_close', cap_color, 12))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.is_video_mode:
            self.reposition_video_overlays()

    def changeEvent(self, event):
        super().changeEvent(event)
        etype = event.type()
        if etype == QEvent.Type.WindowStateChange:
            self.update_max_button()
            apply_win11_frameless_attributes(self, getattr(self, 'is_light', False))
            if self.is_video_mode:
                self.reposition_video_overlays()
        elif etype in (QEvent.Type.ActivationChange, QEvent.Type.PaletteChange, QEvent.Type.ApplicationPaletteChange):
            self.check_system_theme()

    def eventFilter(self, obj, event):
        try:
            if getattr(self, 'is_video_mode', False):
                etype = event.type()
                if etype == QEvent.Type.MouseMove:
                    self.handle_video_mouse_move(event)
                elif etype == QEvent.Type.MouseButtonDblClick:
                    if obj is self.video or (isinstance(obj, QWidget) and self.video.isAncestorOf(obj)):
                        self.fullscreen()
                        return True
        except (RuntimeError, AttributeError):
            return False
        try:
            return super().eventFilter(obj, event)
        except RuntimeError:
            return False

    def nativeEvent(self, eventType, message):
        if eventType in (b'windows_generic_MSG', b'windows_dispatcher_MSG'):
            try:
                msg = wintypes.MSG.from_address(int(message))
                if msg.message in (0x001A, 0x0320):  # WM_SETTINGCHANGE, WM_DWMCOLORIZATIONCOLORCHANGED
                    self.check_system_theme()
                elif msg.message == 0x0084:  # WM_NCHITTEST
                    x = ctypes.c_short(msg.lParam & 0xffff).value
                    y = ctypes.c_short((msg.lParam >> 16) & 0xffff).value
                    local = self.mapFromGlobal(QPoint(x, y))
                    w = self.width()
                    h = self.height()
                    border = 6
                    # Resize handles on borders when not maximized and not fullscreen
                    if not self.isMaximized() and not self.isFullScreen():
                        if local.x() < border and local.y() < border:
                            return True, 13  # HTTOPLEFT
                        if local.x() > w - border and local.y() < border:
                            return True, 14  # HTTOPRIGHT
                        if local.x() < border and local.y() > h - border:
                            return True, 16  # HTBOTTOMLEFT
                        if local.x() > w - border and local.y() > h - border:
                            return True, 17  # HTBOTTOMRIGHT
                        if local.y() < border:
                            return True, 12  # HTTOP
                        if local.y() > h - border:
                            return True, 15  # HTBOTTOM
                        if local.x() < border:
                            return True, 10  # HTLEFT
                        if local.x() > w - border:
                            return True, 11  # HTRIGHT
                    # Drag area: top 58px when not fullscreen and not over buttons or inputs
                    if not self.isFullScreen() and local.y() < 58:
                        child = self.childAt(local)
                        if child is None or not isinstance(child, (QPushButton, QLineEdit, QComboBox)):
                            return True, 2  # HTCAPTION
                    return True, 1  # HTCLIENT
            except Exception:
                pass
        return super().nativeEvent(eventType, message)

    def shortcuts_dialog(self):
        FluentDialog.shortcuts(self)

    def about(self):
        FluentDialog.about(self, self.engine.version, self.library.directory)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        files = []
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if path and Path(path).is_dir():
                self.scan_folder(path)
            else:
                files.append(path or url.toString())
        if files:
            self.import_paths(files)
        event.acceptProposedAction()

    def closeEvent(self, event):
        app = QApplication.instance()
        if app:
            try:
                app.removeEventFilter(self)
            except RuntimeError:
                pass
        if self.scanner and self.scanner.isRunning():
            self.scanner.requestInterruption()
            self.scanner.wait()
        if self.meta_scanner and self.meta_scanner.isRunning():
            self.meta_scanner.requestInterruption()
            self.meta_scanner.wait()
        self.timer.stop()
        self.store_position()
        self.save()
        self.engine.close()
        event.accept()


def main():
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('OcalSoftware.OcalMediaPlayer')
    except Exception:
        pass
    app = QApplication(sys.argv)
    app.setApplicationName('Ocal Media Player')
    app.setOrganizationName('Ocal Software under Gaming Network Studio')
    icon_path = ROOT / 'assets' / 'app-icon.ico'
    if icon_path.is_file():
        app.setWindowIcon(QIcon(str(icon_path)))
    QFontDatabase.addApplicationFont(str(ROOT / 'assets' / 'PlusJakartaSans.ttf'))
    app.setStyle('Fusion')

    lib = Library()
    user_mode = lib.settings.get('theme_mode', 'system')
    if user_mode == 'dark':
        is_light = False
    elif user_mode == 'light':
        is_light = True
    else:
        is_light = is_windows_light_theme()

    user_accent = lib.settings.get('accent_color', 'system')
    if user_accent and user_accent.lower() != 'system':
        palette = make_accent_palette(user_accent, is_light)
    else:
        palette = get_windows_accent_palette(is_light)

    app.setStyleSheet(get_stylesheet(palette, is_light))
    try:
        window = PlayerWindow(library=lib)
    except Exception as exc:
        QMessageBox.critical(None, 'Ocal Media Player could not start', str(exc))
        return 1
    window.show()
    apply_win11_frameless_attributes(window, is_light)
    if len(sys.argv) > 1:
        items = window.import_paths(sys.argv[1:])
        if items:
            window.start_queue(items)
    return app.exec()
