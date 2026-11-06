"""Vector icon generator for Windows 11 Media Player. Pure QPainter vector rendering."""
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QPen, QBrush, QPainterPath, QFont
from PySide6.QtCore import Qt, QRectF, QPointF, QSize

_CACHE = {}


def get_icon(name, color='#ffffff', size=24):
    """Return a cached QIcon rendered via vector QPainter paths without emoji or font dependencies."""
    key = (name, color, size)
    if key in _CACHE:
        return _CACHE[key]

    pix = QPixmap(size, size)
    pix.fill(Qt.GlobalColor.transparent)
    p = QPainter(pix)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)

    # Scale painter to normalized 24x24 coordinate system
    scale = size / 24.0
    p.scale(scale, scale)

    pen = QPen(QColor(color), 1.6, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
    p.setPen(pen)
    brush = QBrush(QColor(color))

    if name == 'home':
        path = QPainterPath()
        path.moveTo(4, 11)
        path.lineTo(12, 4.5)
        path.lineTo(20, 11)
        path.lineTo(17.5, 11)
        path.lineTo(17.5, 19)
        path.lineTo(6.5, 19)
        path.lineTo(6.5, 11)
        path.closeSubpath()
        p.drawPath(path)
    elif name in {'arrow_left', 'back'}:
        p.drawLine(6, 12, 18, 12)
        p.drawLine(6, 12, 11, 7)
        p.drawLine(6, 12, 11, 17)
    elif name == 'music':
        p.setBrush(brush)
        p.drawEllipse(QRectF(5, 13.5, 5, 4))
        p.drawEllipse(QRectF(14, 11.5, 5, 4))
        p.drawLine(10, 15, 10, 5.5)
        p.drawLine(19, 13, 19, 4)
        p.drawLine(10, 5.5, 19, 4)
        p.drawLine(10, 7.5, 19, 6)
    elif name == 'video':
        p.drawRoundedRect(QRectF(4, 5, 16, 14), 2.5, 2.5)
        p.setBrush(brush)
        path = QPainterPath()
        path.moveTo(10, 8.5)
        path.lineTo(15.5, 12)
        path.lineTo(10, 15.5)
        path.closeSubpath()
        p.drawPath(path)
    elif name == 'heart_outline':
        path = QPainterPath()
        path.moveTo(12, 18.5)
        path.cubicTo(6, 13.5, 3.5, 10, 3.5, 7.5)
        path.cubicTo(3.5, 5, 5.5, 3.8, 7.8, 3.8)
        path.cubicTo(9.8, 3.8, 11.2, 4.8, 12, 6)
        path.cubicTo(12.8, 4.8, 14.2, 3.8, 16.2, 3.8)
        path.cubicTo(18.5, 3.8, 20.5, 5, 20.5, 7.5)
        path.cubicTo(20.5, 10, 18, 13.5, 12, 18.5)
        p.drawPath(path)
    elif name == 'heart_fill':
        p.setBrush(brush)
        path = QPainterPath()
        path.moveTo(12, 18.5)
        path.cubicTo(6, 13.5, 3.5, 10, 3.5, 7.5)
        path.cubicTo(3.5, 5, 5.5, 3.8, 7.8, 3.8)
        path.cubicTo(9.8, 3.8, 11.2, 4.8, 12, 6)
        path.cubicTo(12.8, 4.8, 14.2, 3.8, 16.2, 3.8)
        path.cubicTo(18.5, 3.8, 20.5, 5, 20.5, 7.5)
        path.cubicTo(20.5, 10, 18, 13.5, 12, 18.5)
        p.drawPath(path)
    elif name == 'history':
        p.drawArc(QRectF(4, 4, 16, 16), 45 * 16, 270 * 16)
        p.drawLine(12, 7.5, 12, 12)
        p.drawLine(12, 12, 15.5, 12)
        p.drawLine(11.5, 3.5, 15, 4.5)
        p.drawLine(15, 4.5, 13.5, 8)
    elif name == 'nowplaying':
        p.setBrush(brush)
        path = QPainterPath()
        path.moveTo(8, 5.5)
        path.lineTo(18, 12)
        path.lineTo(8, 18.5)
        path.closeSubpath()
        p.drawPath(path)
    elif name == 'keyboard':
        p.drawRoundedRect(QRectF(3, 6, 18, 12), 2.5, 2.5)
        p.drawLine(8, 14, 16, 14)
        p.drawLine(6, 10, 8, 10)
        p.drawLine(11, 10, 13, 10)
        p.drawLine(16, 10, 18, 10)
    elif name == 'info':
        p.drawEllipse(QRectF(3.5, 3.5, 17, 17))
        p.setBrush(brush)
        p.drawEllipse(QRectF(11, 7, 2, 2))
        p.drawLine(12, 11, 12, 16.5)
    elif name == 'open_files':
        path = QPainterPath()
        path.moveTo(4, 7)
        path.lineTo(9, 7)
        path.lineTo(11, 9)
        path.lineTo(19, 9)
        path.lineTo(19, 18)
        path.lineTo(4, 18)
        path.closeSubpath()
        p.drawPath(path)
        p.drawLine(11.5, 11.5, 11.5, 15.5)
        p.drawLine(9.5, 13.5, 13.5, 13.5)
    elif name == 'folder':
        path = QPainterPath()
        path.moveTo(4, 7)
        path.lineTo(9.5, 7)
        path.lineTo(11.5, 9)
        path.lineTo(19.5, 9)
        path.lineTo(19.5, 18)
        path.lineTo(4, 18)
        path.closeSubpath()
        p.drawPath(path)
    elif name == 'stream':
        p.drawEllipse(QRectF(4, 4, 16, 16))
        p.drawLine(4, 12, 20, 12)
        p.drawArc(QRectF(7.5, 4, 9, 16), 0, 360 * 16)
    elif name == 'shuffle':
        p.drawLine(4, 7, 8.5, 7)
        p.drawLine(8.5, 7, 15.5, 17)
        p.drawLine(15.5, 17, 19.5, 17)
        p.drawLine(17, 14.5, 19.5, 17)
        p.drawLine(17, 19.5, 19.5, 17)
        p.drawLine(4, 17, 8.5, 17)
        p.drawLine(8.5, 17, 11.2, 12.8)
        p.drawLine(12.8, 11.2, 15.5, 7)
        p.drawLine(15.5, 7, 19.5, 7)
        p.drawLine(17, 4.5, 19.5, 7)
        p.drawLine(17, 9.5, 19.5, 7)
    elif name == 'repeat':
        p.drawArc(QRectF(5, 6, 14, 12), 40 * 16, 280 * 16)
        p.drawLine(15.5, 4.5, 19, 7)
        p.drawLine(19, 7, 15.5, 9.5)
    elif name == 'refresh':
        p.drawArc(QRectF(4, 4, 16, 16), 40 * 16, 280 * 16)
        p.drawLine(15.5, 3.2, 19, 6)
        p.drawLine(19, 6, 16, 9.2)
    elif name == 'prev':
        p.drawLine(6, 6, 6, 18)
        p.setBrush(brush)
        path = QPainterPath()
        path.moveTo(18, 6.5)
        path.lineTo(8, 12)
        path.lineTo(18, 17.5)
        path.closeSubpath()
        p.drawPath(path)
    elif name == 'next':
        p.drawLine(18, 6, 18, 18)
        p.setBrush(brush)
        path = QPainterPath()
        path.moveTo(6, 6.5)
        path.lineTo(16, 12)
        path.lineTo(6, 17.5)
        path.closeSubpath()
        p.drawPath(path)
    elif name == 'back10':
        p.drawArc(QRectF(4, 4, 16, 16), 45 * 16, 270 * 16)
        p.drawLine(12.5, 3.2, 15.5, 4.8)
        p.drawLine(15.5, 4.8, 13.8, 8)
        f = QFont('Segoe UI', 6, QFont.Weight.Bold)
        p.setFont(f)
        p.drawText(QRectF(5, 7, 14, 11), Qt.AlignmentFlag.AlignCenter, '10')
    elif name == 'fwd10':
        p.drawArc(QRectF(4, 4, 16, 16), -45 * 16, -270 * 16)
        p.drawLine(11.5, 3.2, 8.5, 4.8)
        p.drawLine(8.5, 4.8, 10.2, 8)
        f = QFont('Segoe UI', 6, QFont.Weight.Bold)
        p.setFont(f)
        p.drawText(QRectF(5, 7, 14, 11), Qt.AlignmentFlag.AlignCenter, '10')
    elif name == 'play':
        p.setBrush(brush)
        path = QPainterPath()
        path.moveTo(8.5, 6)
        path.lineTo(17.5, 12)
        path.lineTo(8.5, 18)
        path.closeSubpath()
        p.drawPath(path)
    elif name == 'pause':
        p.setBrush(brush)
        p.drawRoundedRect(QRectF(7.5, 5.5, 3, 13), 1.5, 1.5)
        p.drawRoundedRect(QRectF(13.5, 5.5, 3, 13), 1.5, 1.5)
    elif name == 'volume':
        p.setBrush(brush)
        path = QPainterPath()
        path.moveTo(5, 9.5)
        path.lineTo(8, 9.5)
        path.lineTo(12, 6)
        path.lineTo(12, 18)
        path.lineTo(8, 14.5)
        path.lineTo(5, 14.5)
        path.closeSubpath()
        p.drawPath(path)
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawArc(QRectF(9.5, 7.5, 6, 9), -45 * 16, 90 * 16)
        p.drawArc(QRectF(9.5, 5, 9, 14), -45 * 16, 90 * 16)
    elif name == 'mute':
        p.setBrush(brush)
        path = QPainterPath()
        path.moveTo(5, 9.5)
        path.lineTo(8, 9.5)
        path.lineTo(12, 6)
        path.lineTo(12, 18)
        path.lineTo(8, 14.5)
        path.lineTo(5, 14.5)
        path.closeSubpath()
        p.drawPath(path)
        p.drawLine(14.5, 9.5, 18.5, 14.5)
        p.drawLine(18.5, 9.5, 14.5, 14.5)
    elif name == 'fullscreen':
        p.drawLine(5, 8.5, 5, 5)
        p.drawLine(5, 5, 8.5, 5)
        p.drawLine(15.5, 5, 19, 5)
        p.drawLine(19, 5, 19, 8.5)
        p.drawLine(5, 15.5, 5, 19)
        p.drawLine(5, 19, 8.5, 19)
        p.drawLine(15.5, 19, 19, 19)
        p.drawLine(19, 19, 19, 15.5)
    elif name == 'more':
        p.setBrush(brush)
        p.drawEllipse(QRectF(5, 11, 2.5, 2.5))
        p.drawEllipse(QRectF(10.75, 11, 2.5, 2.5))
        p.drawEllipse(QRectF(16.5, 11, 2.5, 2.5))
    elif name == 'bookmark':
        path = QPainterPath()
        path.moveTo(6.5, 4.5)
        path.lineTo(17.5, 4.5)
        path.lineTo(17.5, 19.5)
        path.lineTo(12, 16)
        path.lineTo(6.5, 19.5)
        path.closeSubpath()
        p.drawPath(path)
    elif name == 'subtitles':
        p.drawRoundedRect(QRectF(4, 6, 16, 12), 2, 2)
        p.drawLine(7.5, 10.5, 16.5, 10.5)
        p.drawLine(7.5, 13.5, 14, 13.5)
    elif name == 'camera':
        path = QPainterPath()
        path.moveTo(4, 8)
        path.lineTo(7, 8)
        path.lineTo(8.5, 6)
        path.lineTo(15.5, 6)
        path.lineTo(17, 8)
        path.lineTo(20, 8)
        path.lineTo(20, 18)
        path.lineTo(4, 18)
        path.closeSubpath()
        p.drawPath(path)
        p.drawEllipse(QRectF(8.5, 9.5, 7, 7))
    elif name == 'cap_min':
        p.drawLine(6, 12, 18, 12)
    elif name == 'cap_max':
        p.drawRect(QRectF(6, 6, 12, 12))
    elif name == 'cap_restore':
        p.drawRect(QRectF(8.5, 5.5, 10, 10))
        p.drawRect(QRectF(5.5, 8.5, 10, 10))
    elif name == 'cap_close':
        p.drawLine(6, 6, 18, 18)
        p.drawLine(18, 6, 6, 18)
    elif name == 'view_list':
        p.drawLine(5, 7, 7, 7)
        p.drawLine(10, 7, 19, 7)
        p.drawLine(5, 12, 7, 12)
        p.drawLine(10, 12, 19, 12)
        p.drawLine(5, 17, 7, 17)
        p.drawLine(10, 17, 19, 17)
    elif name == 'view_grid':
        p.drawRoundedRect(QRectF(4.5, 4.5, 6.5, 6.5), 1.5, 1.5)
        p.drawRoundedRect(QRectF(13, 4.5, 6.5, 6.5), 1.5, 1.5)
        p.drawRoundedRect(QRectF(4.5, 13, 6.5, 6.5), 1.5, 1.5)
        p.drawRoundedRect(QRectF(13, 13, 6.5, 6.5), 1.5, 1.5)
    elif name in {'settings', 'gear'}:
        p.drawEllipse(QRectF(8, 8, 8, 8))
        import math
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            x1 = 12 + 4.5 * math.cos(rad)
            y1 = 12 + 4.5 * math.sin(rad)
            x2 = 12 + 8.2 * math.cos(rad)
            y2 = 12 + 8.2 * math.sin(rad)
            p.drawLine(QPointF(x1, y1), QPointF(x2, y2))
    elif name == 'check':
        p.drawLine(5, 12, 10, 17)
        p.drawLine(10, 17, 19, 7)
    elif name == 'download':
        p.drawLine(12, 4, 12, 16)
        p.drawLine(7, 11, 12, 16)
        p.drawLine(17, 11, 12, 16)
        p.drawLine(4, 19, 20, 19)
    elif name == 'palette':
        p.drawEllipse(QRectF(4, 4, 16, 16))
        p.setBrush(brush)
        p.drawEllipse(QRectF(8, 8, 2, 2))
        p.drawEllipse(QRectF(14, 8, 2, 2))
        p.drawEllipse(QRectF(8, 14, 2, 2))
        p.drawEllipse(QRectF(14, 14, 2, 2))

    p.end()
    icon = QIcon(pix)
    _CACHE[key] = icon
    return icon

