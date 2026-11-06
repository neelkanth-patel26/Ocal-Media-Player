"""Integration check using generated silent audio and a real VLC 4 player."""
import os
import sys
import time
import wave
import shutil
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase
from src.app import PlayerWindow
from src.engine import ROOT
from src.library import Library
from src.theme import STYLE

data = ROOT / '.test-data'
data.mkdir(exist_ok=True)
for name, duration in [('Test silence.wav', 12), ('Next track.wav', 2)]:
    with wave.open(str(data / name), 'wb') as f:
        f.setparams((1, 2, 44100, 0, 'NONE', 'not compressed'))
        f.writeframes(b'\0\0' * 44100 * duration)

app = QApplication([])
app.setStyle('Fusion')
QFontDatabase.addApplicationFont(str(ROOT / 'assets' / 'PlusJakartaSans.ttf'))
app.setStyleSheet(STYLE)
library_path = data / 'library'
if (library_path / 'library.json').exists():
    (library_path / 'library.json').unlink()
window = PlayerWindow(Library(library_path))
window.show()


def wait_until(predicate, timeout=8):
    end = time.monotonic() + timeout
    while time.monotonic() < end:
        app.processEvents()
        if predicate():
            return
        time.sleep(.02)
    raise AssertionError(f'Timed out; state={window.engine.state}, time={window.engine.time}, length={window.engine.length}')


try:
    app.processEvents()
    window.grab().save(str(ROOT / 'assets' / 'player-preview.png'))
    tracks = window.import_paths([str(data / 'Test silence.wav'), str(data / 'Next track.wav')])
    window.start_queue(tracks)
    wait_until(lambda: window.has_played and window.engine.time > 400)
    assert 11900 <= window.engine.length <= 12100, window.engine.length
    window.toggle_play()
    wait_until(lambda: window.engine.state == 3)
    window.engine.seek(6000)
    wait_until(lambda: abs(window.engine.time - 6000) < 500)
    window.store_position()
    assert window.current['position'] >= 5500
    window.toggle_play()
    wait_until(lambda: window.engine.state == 2)
    wait_until(lambda: window.engine.time >= 5500)
    window.a, window.b = 1000, 2000
    window.engine.seek(2200)
    wait_until(lambda: 900 <= window.engine.time < 2100)
    window.a = window.b = None
    window.favorite(tracks[0])
    window.navigate('Favorites')
    assert window.table.rowCount() == 1
    window.search.setText('no matching title')
    assert window.table.rowCount() == 0
    window.search.clear()
    window.set_sleep(1)
    window.sleep_deadline = time.monotonic() - 1
    wait_until(lambda: window.engine.state == 3)
    window.toggle_play()
    wait_until(lambda: window.engine.state == 2)
    window.engine.seek(11500)
    wait_until(lambda: window.current is tracks[1] and window.engine.state == 2)
    wait_until(lambda: window.engine.state == 4)
    assert tracks[1]['position'] == 0
    tracks[0]['position'] = 6000
    window.start_queue([tracks[0]])
    wait_until(lambda: window.has_played and window.pending_resume == 0 and window.engine.time >= 5500)
    window.start_queue([tracks[1]])
    wait_until(lambda: window.has_played and window.engine.length == 2000)
    window.start_queue([tracks[0]])
    wait_until(lambda: window.has_played and window.engine.length == 12000)
    print('PASS: VLC 4 playback, time units, pause, seek, resume persistence, A-B loop, favorites, search, sleep timer, auto-next and completion')
finally:
    window.close()
    app.processEvents()
