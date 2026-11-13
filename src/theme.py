"""Windows 11 Fluent Design stylesheet for Ocal Media Player with Light & Dark mode support."""
from .win11 import get_windows_accent_palette, is_windows_light_theme


def get_stylesheet(palette=None, is_light=None, custom_accent_hex=None):
    """Generate dynamic Windows 11 Fluent stylesheet matching OS theme mode & accent palette."""
    if is_light is None:
        is_light = is_windows_light_theme()

    if palette is None:
        palette = get_windows_accent_palette(is_light, custom_accent_hex=custom_accent_hex)

    accent = palette.get('accent', '#0078d4' if is_light else '#60cdff')
    hover = palette.get('hover', '#106ebe' if is_light else '#78d5ff')
    pressed = palette.get('pressed', '#005a9e' if is_light else '#49b3e8')
    base = palette.get('base', '#0078d4')
    text = palette.get('text', '#ffffff' if is_light else '#000000')
    r, g, b = palette.get('rgb', (0, 120, 212) if is_light else (96, 205, 255))

    if is_light:
        # Windows 11 Fluent Light Mode Palette
        bg_main = '#f3f3f3'
        bg_sidebar = '#f3f3f3'
        bg_card = '#ffffff'
        bg_queue = '#ffffff'
        bg_transport = '#ffffff'
        bg_transport_floating = 'rgba(255, 255, 255, 0.95)'
        bg_drawer = 'rgba(243, 243, 243, 0.96)'

        border_sidebar = '1px solid rgba(0, 0, 0, 0.08)'
        border_drawer = '1px solid rgba(0, 0, 0, 0.12)'
        border_card = '1px solid rgba(0, 0, 0, 0.08)'
        border_transport = '1px solid rgba(0, 0, 0, 0.08)'
        border_transport_floating = '1px solid rgba(0, 0, 0, 0.14)'
        border_video_top = '1px solid rgba(0, 0, 0, 0.08)'

        text_primary = '#1b1b1b'
        text_strong = '#111111'
        text_secondary = '#444444'
        text_muted = '#616161'
        text_disabled = '#9e9e9e'

        btn_bg = 'rgba(0, 0, 0, 0.03)'
        btn_border = '1px solid rgba(0, 0, 0, 0.08)'
        btn_hover = 'rgba(0, 0, 0, 0.06)'
        btn_hover_border = 'rgba(0, 0, 0, 0.14)'
        btn_pressed = 'rgba(0, 0, 0, 0.02)'
        btn_disabled_bg = 'rgba(0, 0, 0, 0.02)'

        nav_text = '#333333'
        nav_hover = 'rgba(0, 0, 0, 0.04)'
        nav_checked_bg = 'rgba(0, 0, 0, 0.06)'
        nav_checked_text = '#111111'

        chip_bg = 'rgba(0, 0, 0, 0.04)'
        chip_border = '1px solid rgba(0, 0, 0, 0.08)'
        chip_text = '#555555'
        chip_hover = 'rgba(0, 0, 0, 0.07)'
        chip_checked_bg = f'rgba({r}, {g}, {b}, 0.14)'
        chip_checked_border = f'rgba({r}, {g}, {b}, 0.35)'

        transport_round_color = '#333333'
        transport_round_hover = 'rgba(0, 0, 0, 0.06)'
        transport_round_checked = f'rgba({r}, {g}, {b}, 0.14)'

        input_bg = '#ffffff'
        input_border = '1px solid rgba(0, 0, 0, 0.14)'
        input_focus_bg = '#ffffff'

        table_item_color = '#1b1b1b'
        table_border = '1px solid rgba(0, 0, 0, 0.04)'
        table_hover = 'rgba(0, 0, 0, 0.04)'
        table_selected = f'rgba({r}, {g}, {b}, 0.12)'
        table_header_bg = '#ffffff'
        table_header_color = '#666666'
        table_header_border = '1px solid rgba(0, 0, 0, 0.08)'

        list_item_color = '#222222'
        list_item_hover = 'rgba(0, 0, 0, 0.04)'
        list_item_selected = f'rgba({r}, {g}, {b}, 0.12)'

        grid_bg = '#ffffff'
        grid_border = '1px solid rgba(0, 0, 0, 0.08)'
        grid_hover = '#fafafa'
        grid_hover_border = 'rgba(0, 0, 0, 0.16)'
        grid_selected = f'rgba({r}, {g}, {b}, 0.12)'
        grid_text = '#1b1b1b'

        slider_groove = 'rgba(0, 0, 0, 0.14)'
        slider_border = '#ffffff'

        scrollbar_handle = 'rgba(0, 0, 0, 0.20)'
        scrollbar_hover = 'rgba(0, 0, 0, 0.35)'

        menu_bg = '#ffffff'
        menu_border = '1px solid rgba(0, 0, 0, 0.12)'
        menu_text = '#111111'
        menu_item_hover = 'rgba(0, 0, 0, 0.05)'
        menu_separator = 'rgba(0, 0, 0, 0.08)'

        tooltip_bg = '#ffffff'
        tooltip_border = '1px solid rgba(0, 0, 0, 0.12)'
        tooltip_text = '#111111'

        caption_btn_color = '#333333'
        caption_btn_hover = 'rgba(0, 0, 0, 0.06)'
        caption_btn_pressed = 'rgba(0, 0, 0, 0.03)'

        dialog_bg = '#f3f3f3'
        dialog_text = '#1b1b1b'

        video_top_bar_bg = 'qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(243, 243, 243, 0.96), stop:1 rgba(243, 243, 243, 0.40))'
    else:
        # Windows 11 Fluent Dark Mode Palette
        bg_main = '#202020'
        bg_sidebar = '#181818'
        bg_card = '#272727'
        bg_queue = '#272727'
        bg_transport = '#212121'
        bg_transport_floating = 'rgba(24, 24, 24, 0.94)'
        bg_drawer = 'rgba(24, 24, 24, 0.96)'

        border_sidebar = '1px solid rgba(255, 255, 255, 0.06)'
        border_drawer = '1px solid rgba(255, 255, 255, 0.12)'
        border_card = '1px solid rgba(255, 255, 255, 0.08)'
        border_transport = '1px solid rgba(255, 255, 255, 0.08)'
        border_transport_floating = '1px solid rgba(255, 255, 255, 0.14)'
        border_video_top = '1px solid rgba(255, 255, 255, 0.08)'

        text_primary = '#f3f3f3'
        text_strong = '#ffffff'
        text_secondary = '#cccccc'
        text_muted = '#9d9d9d'
        text_disabled = '#555555'

        btn_bg = 'rgba(255, 255, 255, 0.06)'
        btn_border = '1px solid rgba(255, 255, 255, 0.08)'
        btn_hover = 'rgba(255, 255, 255, 0.10)'
        btn_hover_border = 'rgba(255, 255, 255, 0.14)'
        btn_pressed = 'rgba(255, 255, 255, 0.04)'
        btn_disabled_bg = 'rgba(255, 255, 255, 0.02)'

        nav_text = '#cccccc'
        nav_hover = 'rgba(255, 255, 255, 0.05)'
        nav_checked_bg = 'rgba(255, 255, 255, 0.08)'
        nav_checked_text = '#ffffff'

        chip_bg = 'rgba(255, 255, 255, 0.05)'
        chip_border = '1px solid rgba(255, 255, 255, 0.08)'
        chip_text = '#a0a0a0'
        chip_hover = 'rgba(255, 255, 255, 0.09)'
        chip_checked_bg = f'rgba({r}, {g}, {b}, 0.18)'
        chip_checked_border = f'rgba({r}, {g}, {b}, 0.40)'

        transport_round_color = '#d0d0d0'
        transport_round_hover = 'rgba(255, 255, 255, 0.08)'
        transport_round_checked = f'rgba({r}, {g}, {b}, 0.20)'

        input_bg = 'rgba(255, 255, 255, 0.06)'
        input_border = '1px solid rgba(255, 255, 255, 0.08)'
        input_focus_bg = 'rgba(255, 255, 255, 0.09)'

        table_item_color = '#e0e0e0'
        table_border = '1px solid rgba(255, 255, 255, 0.04)'
        table_hover = 'rgba(255, 255, 255, 0.04)'
        table_selected = f'rgba({r}, {g}, {b}, 0.14)'
        table_header_bg = '#272727'
        table_header_color = '#8d8d8d'
        table_header_border = '1px solid rgba(255, 255, 255, 0.08)'

        list_item_color = '#d0d0d0'
        list_item_hover = 'rgba(255, 255, 255, 0.05)'
        list_item_selected = f'rgba({r}, {g}, {b}, 0.16)'

        grid_bg = '#272727'
        grid_border = '1px solid rgba(255, 255, 255, 0.07)'
        grid_hover = 'rgba(255, 255, 255, 0.08)'
        grid_hover_border = 'rgba(255, 255, 255, 0.16)'
        grid_selected = f'rgba({r}, {g}, {b}, 0.18)'
        grid_text = '#f3f3f3'

        slider_groove = 'rgba(255, 255, 255, 0.20)'
        slider_border = '#212121'

        scrollbar_handle = 'rgba(255, 255, 255, 0.20)'
        scrollbar_hover = 'rgba(255, 255, 255, 0.35)'

        menu_bg = '#272727'
        menu_border = '1px solid rgba(255, 255, 255, 0.12)'
        menu_text = '#ffffff'
        menu_item_hover = 'rgba(255, 255, 255, 0.08)'
        menu_separator = 'rgba(255, 255, 255, 0.08)'

        tooltip_bg = '#2b2b2b'
        tooltip_border = '1px solid rgba(255, 255, 255, 0.12)'
        tooltip_text = '#ffffff'

        caption_btn_color = '#cccccc'
        caption_btn_hover = 'rgba(255, 255, 255, 0.09)'
        caption_btn_pressed = 'rgba(255, 255, 255, 0.05)'

        dialog_bg = '#242424'
        dialog_text = '#ffffff'

        video_top_bar_bg = 'qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(16, 16, 16, 0.95), stop:1 rgba(16, 16, 16, 0.40))'

    return f"""
QWidget {{
    color: {text_primary};
    font-family: "Segoe UI Variable Text", "Segoe UI", "Plus Jakarta Sans", -apple-system, sans-serif;
    font-size: 12px;
}}
QMainWindow, QWidget#canvas {{
    background: {bg_main};
}}
QFrame#sidebar {{
    background: {bg_sidebar};
    border-right: {border_sidebar};
}}
QFrame#left_drawer {{
    background: {bg_drawer};
    border-right: {border_drawer};
}}
QFrame#left_drawer QFrame#sidebar {{
    background: transparent;
    border: none;
}}
QFrame#card, QFrame#queue {{
    background: {bg_card};
    border: {border_card};
    border-radius: 8px;
}}
QFrame#right_drawer {{
    background: {bg_drawer};
    border-left: {border_drawer};
}}
QFrame#right_drawer QFrame#queue {{
    background: transparent;
    border: none;
}}
QFrame#video_top_bar {{
    background: {video_top_bar_bg};
    border-bottom: {border_video_top};
}}
QFrame#transport {{
    background: {bg_transport};
    border: none;
    border-top: {border_transport};
    border-radius: 0px;
}}
QFrame#transport[floating="true"] {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0.0 rgba(0, 0, 0, 0.0),
        stop:0.25 rgba(15, 15, 15, 0.70),
        stop:0.6 rgba(15, 15, 15, 0.88),
        stop:1.0 rgba(15, 15, 15, 0.96));
    border: none;
    border-radius: 0px;
}}
QFrame#transport[floating="true"] QPushButton#transport_round {{
    color: #ffffff;
    qproperty-iconSize: 20px 20px;
}}
QFrame#transport[floating="true"] QPushButton#transport_round:hover {{
    background: rgba(255, 255, 255, 0.14);
}}
QFrame#transport[floating="true"] QPushButton#transport_round:pressed {{
    background: rgba(255, 255, 255, 0.24);
}}
QFrame#transport[floating="true"] QSlider::groove:horizontal {{
    height: 4px;
    background: rgba(255, 255, 255, 0.30);
    border-radius: 2px;
}}
QFrame#transport[floating="true"] QSlider::sub-page:horizontal {{
    background: {accent};
    border-radius: 2px;
}}
QFrame#transport[floating="true"] QSlider::handle:horizontal {{
    background: #ffffff;
    width: 14px;
    height: 14px;
    margin: -5px 0;
    border-radius: 7px;
    border: 2px solid {accent};
}}
QFrame#transport[floating="true"] QSlider::handle:horizontal:hover {{
    background: {accent};
    width: 16px;
    height: 16px;
    margin: -6px 0;
    border-radius: 8px;
    border: 2px solid #ffffff;
}}
QLabel {{
    background: transparent;
    color: {text_primary};
}}
QLabel#brand {{
    font-size: 15px;
    font-weight: 700;
    color: {text_strong};
    letter-spacing: -0.2px;
}}
QLabel#eyebrow {{
    font-size: 10px;
    color: {accent};
    font-weight: 700;
    letter-spacing: 1.5px;
}}
QLabel#heading {{
    font-size: 26px;
    font-weight: 600;
    color: {text_strong};
    letter-spacing: -0.5px;
}}
QLabel#muted {{
    color: {text_muted};
    font-size: 11px;
}}
QLabel#section {{
    font-size: 15px;
    font-weight: 600;
    color: {text_strong};
}}
QLabel#badge {{
    background: rgba({r}, {g}, {b}, 0.15);
    color: {accent};
    border-radius: 6px;
    padding: 4px 8px;
    font-size: 10px;
    font-weight: 600;
}}
QPushButton {{
    background: {btn_bg};
    color: {text_primary};
    border: {btn_border};
    border-radius: 6px;
    padding: 7px 14px;
    font-weight: 500;
    font-size: 12px;
}}
QPushButton:hover {{
    background: {btn_hover};
    border-color: {btn_hover_border};
}}
QPushButton:pressed {{
    background: {btn_pressed};
    border-color: {btn_border};
}}
QPushButton:focus {{
    border: 2px solid {accent};
}}
QPushButton:disabled {{
    color: {text_disabled};
    background: {btn_disabled_bg};
    border-color: transparent;
}}
QPushButton#primary {{
    background: {accent};
    color: {text};
    border: 1px solid {accent};
    font-weight: 600;
}}
QPushButton#primary:hover {{
    background: {hover};
    border-color: {hover};
}}
QPushButton#primary:pressed {{
    background: {pressed};
    border-color: {pressed};
}}
QPushButton#nav {{
    text-align: left;
    border: 1px solid transparent;
    background: transparent;
    padding: 10px 14px;
    min-height: 24px;
    border-radius: 10px;
    color: {nav_text};
    font-size: 13px;
    font-weight: 500;
    qproperty-iconSize: 24px 24px;
}}
QPushButton#nav:checked {{
    background: {accent};
    color: {text};
    border-color: {accent};
    font-weight: 600;
}}
QPushButton#nav:hover {{
    background: {nav_hover};
    color: {nav_checked_text};
    border-color: {btn_hover_border};
}}
QPushButton#nav:checked:hover {{
    background: {hover};
    color: {text};
    border-color: {hover};
}}
QPushButton#nav:pressed {{
    background: rgba({r}, {g}, {b}, 0.25);
}}
QPushButton#nav:checked:pressed {{
    background: {pressed};
    color: {text};
    border-color: {pressed};
}}
QPushButton#nav:focus {{
    border: 1px solid {accent};
}}
QPushButton#chip {{
    border-radius: 13px;
    padding: 5px 12px;
    font-size: 11px;
    background: {chip_bg};
    border: {chip_border};
    color: {chip_text};
}}
QPushButton#chip:hover {{
    background: {chip_hover};
    color: {text_strong};
}}
QPushButton#chip:checked {{
    color: {text};
    background: {accent};
    border: 1px solid {accent};
    font-weight: 600;
}}
QPushButton#chip:checked:hover {{
    background: {hover};
    border-color: {hover};
    color: {text};
}}
QPushButton#chip:checked:pressed {{
    background: {pressed};
    border-color: {pressed};
    color: {text};
}}
QPushButton#transport_round {{
    background: transparent;
    border: none;
    border-radius: 17px;
    padding: 4px;
    color: {transport_round_color};
    qproperty-iconSize: 20px 20px;
}}
QPushButton#transport_round:hover {{
    background: {transport_round_hover};
    color: {text_strong};
}}
QPushButton#transport_round:checked {{
    background: {transport_round_checked};
    color: {accent};
}}
QPushButton#play {{
    background: {accent};
    color: {text};
    border: none;
    border-radius: 23px;
    qproperty-iconSize: 20px 20px;
}}
QPushButton#play:hover {{
    background: {hover};
}}
QPushButton#play:pressed {{
    background: {pressed};
}}
QPushButton#caption_btn {{
    background: transparent;
    border: none;
    border-radius: 6px;
    padding: 0px;
    min-width: 38px;
    max-width: 38px;
    min-height: 32px;
    max-height: 32px;
    color: {caption_btn_color};
    qproperty-iconSize: 12px 12px;
}}
QPushButton#caption_btn:hover {{
    background: {caption_btn_hover};
    color: {text_strong};
}}
QPushButton#caption_btn:pressed {{
    background: {caption_btn_pressed};
}}
QPushButton#caption_close {{
    background: transparent;
    border: none;
    border-radius: 6px;
    padding: 0px;
    min-width: 38px;
    max-width: 38px;
    min-height: 32px;
    max-height: 32px;
    color: {caption_btn_color};
    qproperty-iconSize: 12px 12px;
}}
QPushButton#caption_close:hover {{
    background: #e81123;
    color: #ffffff;
}}
QPushButton#caption_close:pressed {{
    background: #c4101f;
    color: #ffffff;
}}
QLineEdit {{
    background: {input_bg};
    border: {input_border};
    border-radius: 8px;
    padding: 8px 14px;
    color: {text_strong};
    selection-background-color: {accent};
    selection-color: {text};
}}
QLineEdit:focus {{
    border: 2px solid {accent};
    background: {input_focus_bg};
}}
QTableWidget {{
    border: none;
    background: transparent;
    gridline-color: transparent;
    selection-background-color: {table_selected};
    selection-color: {text_strong};
    outline: none;
}}
QTableWidget::item {{
    padding: 8px 10px;
    border-radius: 0px;
    border-bottom: {table_border};
    color: {table_item_color};
}}
QTableWidget::item:hover {{
    background: {table_hover};
    border-radius: 0px;
}}
QTableWidget::item:selected {{
    background: {table_selected};
    color: {text_strong};
    border-radius: 0px;
}}
QHeaderView::section {{
    color: {table_header_color};
    background: {table_header_bg};
    border: none;
    border-bottom: {table_header_border};
    padding: 8px 10px;
    font-size: 10px;
    font-weight: 600;
}}
QListWidget {{
    background: transparent;
    border: none;
    outline: none;
}}
QListWidget::item {{
    padding: 8px 10px;
    border-radius: 6px;
    margin-bottom: 3px;
    color: {list_item_color};
}}
QListWidget::item:hover {{
    background: {list_item_hover};
    color: {text_strong};
}}
QListWidget::item:selected {{
    background: {list_item_selected};
    color: {accent};
}}
QComboBox {{
    border: {btn_border};
    border-radius: 6px;
    padding: 5px 12px;
    background: {btn_bg};
    color: {text_strong};
}}
QComboBox:hover {{
    background: {btn_hover};
}}
QComboBox::drop-down {{
    border: none;
    width: 18px;
}}
QComboBox QAbstractItemView {{
    background: {bg_card};
    border: {menu_border};
    border-radius: 6px;
    color: {text_strong};
    selection-background-color: {chip_checked_bg};
    selection-color: {accent};
    padding: 4px;
    outline: none;
}}
QSlider::groove:horizontal {{
    height: 4px;
    background: {slider_groove};
    border-radius: 2px;
}}
QSlider::sub-page:horizontal {{
    background: {accent};
    border-radius: 2px;
}}
QSlider::handle:horizontal {{
    background: {accent};
    width: 14px;
    height: 14px;
    margin: -5px 0;
    border-radius: 7px;
    border: 2px solid {slider_border};
}}
QSlider::handle:horizontal:hover {{
    background: {hover};
    width: 16px;
    height: 16px;
    margin: -6px 0;
    border-radius: 8px;
}}
QScrollBar:vertical {{
    width: 6px;
    background: transparent;
}}
QScrollBar::handle:vertical {{
    background: {scrollbar_handle};
    border-radius: 3px;
    min-height: 25px;
}}
QScrollBar::handle:vertical:hover {{
    background: {scrollbar_hover};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}
QScrollBar:horizontal {{
    height: 0px;
    width: 0px;
    background: transparent;
    border: none;
}}
QScrollBar::handle:horizontal,
QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal,
QScrollBar::add-page:horizontal,
QScrollBar::sub-page:horizontal {{
    width: 0px;
    height: 0px;
    background: transparent;
    border: none;
}}
QListWidget#grid_view {{
    background: transparent;
    border: none;
    outline: none;
    padding: 6px 2px;
}}
QListWidget#grid_view::item {{
    background: {grid_bg};
    border: {grid_border};
    border-radius: 10px;
    padding: 10px;
    color: {grid_text};
    font-size: 11px;
    font-weight: 500;
    text-align: center;
}}
QListWidget#grid_view::item:hover {{
    background: {grid_hover};
    border-color: {grid_hover_border};
}}
QListWidget#grid_view::item:selected {{
    background: {grid_selected};
    border: 1px solid {accent};
    color: {text_strong};
}}
QPushButton#view_toggle {{
    background: {btn_bg};
    border: {btn_border};
    border-radius: 6px;
    padding: 5px 8px;
    min-width: 32px;
    max-width: 32px;
    min-height: 28px;
    max-height: 28px;
    qproperty-iconSize: 16px 16px;
}}
QPushButton#view_toggle:hover {{
    background: {btn_hover};
    border-color: {btn_hover_border};
}}
QPushButton#view_toggle:checked {{
    background: {accent};
    border: 1px solid {accent};
    color: {text};
}}
QPushButton#view_toggle:checked:hover {{
    background: {hover};
    border-color: {hover};
    color: {text};
}}
QPushButton#view_toggle:checked:pressed {{
    background: {pressed};
    border-color: {pressed};
    color: {text};
}}
QMenu {{
    background: {menu_bg};
    border: {menu_border};
    border-radius: 8px;
    padding: 6px;
    color: {menu_text};
}}
QMenu::item {{
    padding: 7px 20px;
    border-radius: 4px;
    color: {menu_text};
}}
QMenu::item:selected {{
    background: {menu_item_hover};
    color: {text_strong};
}}
QMenu::separator {{
    height: 1px;
    background: {menu_separator};
    margin: 4px 0;
}}
QToolTip {{
    background: {tooltip_bg};
    color: {tooltip_text};
    border: {tooltip_border};
    border-radius: 4px;
    padding: 5px 8px;
    font-size: 11px;
}}
QDialog, QMessageBox {{
    background: {dialog_bg};
    color: {dialog_text};
}}
"""


STYLE = get_stylesheet()
