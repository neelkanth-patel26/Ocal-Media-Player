"""Generate a tiny uncompressed AVI, verify embedded video and subtitle loading."""
import struct
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from PySide6.QtWidgets import QApplication
from src.app import PlayerWindow
from src.engine import ROOT
from src.library import Library
from src.theme import STYLE


def chunk(tag, payload):
    return tag + struct.pack('<I', len(payload)) + payload + (b'\0' if len(payload) % 2 else b'')


def make_video(path):
    width, height, fps, count = 320, 180, 10, 80
    size = width * height * 3
    avih = struct.pack('<14I', 1000000 // fps, size * fps, 0, 0, count, 0, 1, size, width, height, 0, 0, 0, 0)
    strh = struct.pack('<4s4sIHH8I4h', b'vids', b'DIB ', 0, 0, 0, 0, 1, fps, 0, count, size, 0xFFFFFFFF, 0, 0, 0, width, height)
    strf = struct.pack('<IiiHHIIiiII', 40, width, height, 1, 24, 0, size, 0, 0, 0, 0)
    header = chunk(b'LIST', b'hdrl' + chunk(b'avih', avih) + chunk(b'LIST', b'strl' + chunk(b'strh', strh) + chunk(b'strf', strf)))
    frames = b''
    for i in range(count):
        # Three distinct color bands make decoded-frame assertions meaningful.
        row = bytes((232, 82, 41)) * 106 + bytes((91, 135, 54)) * 107 + bytes((92, 183, 232)) * 107
        frames += chunk(b'00db', row * height)
    path.write_bytes(chunk(b'RIFF', b'AVI ' + header + chunk(b'LIST', b'movi' + frames)))


data = ROOT / '.test-data'
data.mkdir(exist_ok=True)
path = data / 'Video test.avi'
make_video(path)
subtitle = data / 'Video test.srt'
subtitle.write_text('1\n00:00:00,000 --> 00:00:07,000\nGNS Player video test\n', encoding='utf-8')
app = QApplication([])
app.setStyleSheet(STYLE)
window = PlayerWindow(Library(data / 'video-library'))
window.show()


def until(fn, timeout=10):
    end = time.monotonic() + timeout
    while time.monotonic() < end:
        app.processEvents()
        if fn():
            return
        time.sleep(.03)
    raise AssertionError('Video condition timed out')


try:
    entry = window.import_paths([str(path)])[0]
    entry['position'] = 0
    window.start_queue([entry])
    until(lambda: window.has_played and window.engine.time > 500)
    assert window.pages.currentIndex() == 1
    assert window.engine.subtitle(str(subtitle)) == 0
    snapshot = data / 'video-frame.png'
    if snapshot.exists():
        snapshot.unlink()
    assert window.engine.snapshot(snapshot) == 0
    until(snapshot.exists)
    from PySide6.QtGui import QImage
    frame = QImage(str(snapshot))
    assert frame.width() == 320 and frame.height() == 180
    assert frame.pixelColor(20, 20).blue() > 200
    assert frame.pixelColor(160, 20).green() > 100
    assert frame.pixelColor(290, 20).red() > 200
    window.fullscreen()
    app.processEvents()
    assert window.isFullScreen()
    window.fullscreen()
    assert not window.isFullScreen()
    print('PASS: embedded VLC video, decoded color pixels, subtitle attachment, PNG snapshot, fullscreen')
finally:
    window.close()
    app.processEvents()
