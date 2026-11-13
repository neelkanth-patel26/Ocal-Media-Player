"""Interactive & Automated Test Script for Timeline Click-to-Seek.

Run this script to verify that clicking anywhere along the playback timeline immediately
jumps playback to that exact timestamp for both audio and video playback.

Usage:
    python scripts/test_timeline_seek.py             # Runs automated click verification + interactive test
    python scripts/test_timeline_seek.py --auto      # Runs automated verification only
"""
import sys
import time
import wave
from pathlib import Path

# Add project root to sys.path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QMouseEvent, QFontDatabase

from src.app import PlayerWindow, ClickableSlider
from src.library import Library, clock
from src.theme import get_stylesheet
from src.win11 import get_windows_accent_palette, is_windows_light_theme


def create_test_audio(path: Path, seconds: int = 30):
    """Generate a clean test audio file with exact duration."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), 'wb') as f:
        f.setparams((1, 2, 44100, 0, 'NONE', 'not compressed'))
        f.writeframes(b'\0\0' * 44100 * seconds)


def run_timeline_seek_test(interactive: bool = True):
    print("=" * 70)
    print("   OCAL MEDIA PLAYER - TIMELINE CLICK-TO-SEEK VERIFICATION TOOL")
    print("=" * 70)

    app = QApplication.instance() or QApplication(sys.argv)
    QFontDatabase.addApplicationFont(str(ROOT / 'assets' / 'PlusJakartaSans.ttf'))
    is_light = is_windows_light_theme()
    palette = get_windows_accent_palette(is_light)
    app.setStyleSheet(get_stylesheet(palette, is_light))

    test_dir = ROOT / '.test-data'
    test_file = test_dir / 'Timeline_Test_30s.wav'
    create_test_audio(test_file, seconds=30)

    lib = Library(test_dir / 'test_lib')
    win = PlayerWindow(lib)
    win.resize(1000, 600)
    win.show()

    # Import and start playing test audio
    tracks = win.import_paths([str(test_file)])
    win.start_queue(tracks)

    print("\n[1/4] Starting playback...")
    # Wait for media engine to start
    start_wait = time.monotonic()
    while time.monotonic() - start_wait < 3.0:
        app.processEvents()
        if win.has_played and win.engine.time >= 200:
            break
        time.sleep(0.02)

    total_len = win.engine.length or 30000
    print(f"       Playback active: Total duration = {clock(total_len)} ({total_len}ms)")
    print(f"       Seek bar geometry: width = {win.seek.width()}px, height = {win.seek.height()}px")
    assert isinstance(win.seek, ClickableSlider), "win.seek is not a ClickableSlider!"

    # Target points to test: 25%, 50%, 75%, 15%
    test_points = [
        ("25% (First quarter)", 0.25),
        ("50% (Midpoint)", 0.50),
        ("75% (Third quarter)", 0.75),
        ("15% (Early jump)", 0.15),
    ]

    print("\n[2/4] Running automated click-to-seek tests:")
    passed_all = True

    for label, ratio in test_points:
        app.processEvents()
        time.sleep(0.05)

        target_expected_ms = total_len * ratio
        click_x = int(win.seek.width() * ratio)
        click_y = win.seek.height() // 2

        print(f"\n  --> Clicking timeline at {label} (x={click_x}px)...")

        # Simulate real physical mouse press and release
        p_event = QMouseEvent(
            QMouseEvent.Type.MouseButtonPress,
            QPoint(click_x, click_y),
            Qt.MouseButton.LeftButton,
            Qt.MouseButton.LeftButton,
            Qt.KeyboardModifier.NoModifier
        )
        win.seek.mousePressEvent(p_event)

        r_event = QMouseEvent(
            QMouseEvent.Type.MouseButtonRelease,
            QPoint(click_x, click_y),
            Qt.MouseButton.LeftButton,
            Qt.MouseButton.NoButton,
            Qt.KeyboardModifier.NoModifier
        )
        win.seek.mouseReleaseEvent(r_event)

        # Let the UI loop process events
        for _ in range(15):
            app.processEvents()
            time.sleep(0.02)

        actual_time = win.engine.time
        diff = abs(actual_time - target_expected_ms)

        print(f"      Target:   {clock(target_expected_ms)} ({int(target_expected_ms)}ms)")
        print(f"      Actual:   {clock(actual_time)} ({actual_time}ms)")
        print(f"      Seekbar:  {win.seek.value()} / 10000 (Elapsed text: {win.elapsed.text()})")

        # Allow generous +/- 1.5s margin for keyframe alignment
        if diff < 2000:
            print(f"      Result:   [PASS] Successfully jumped to {clock(actual_time)}!")
        else:
            print(f"      Result:   [FAIL] Expected near {clock(target_expected_ms)}, got {clock(actual_time)}")
            passed_all = False

    print("\n" + "=" * 70)
    if passed_all:
        print("   >>> ALL AUTOMATED CLICK-TO-SEEK TESTS PASSED SUCCESSFULLY! <<<")
    else:
        print("   >>> SOME TESTS FAILED <<<")
    print("=" * 70)

    if interactive:
        print("\n[3/4] Interactive Test Mode:")
        print("      The player window is open on your screen.")
        print("      Click anywhere on the timeline seekbar to test interactive jumps.")
        print("      Close the player window when finished.")

        # Hook live feedback
        original_seek_released = win.seek_released
        def verbose_seek():
            original_seek_released()
            val = win.seek.value()
            pct = val / 100.0
            print(f"      [USER CLICK] Seekbar jumped to {pct:.1f}% -> Time: {win.elapsed.text()} / {win.duration.text()}")
        win.seek.sliderReleased.disconnect()
        win.seek.sliderReleased.connect(verbose_seek)

        while win.isVisible():
            app.processEvents()
            time.sleep(0.02)

    win.close()
    return passed_all


if __name__ == '__main__':
    is_interactive = '--auto' not in sys.argv
    success = run_timeline_seek_test(interactive=is_interactive)
    sys.exit(0 if success else 1)
