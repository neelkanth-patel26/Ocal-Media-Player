"""Unit tests for ClickableSlider direct click-to-seek, smooth scrubbing, and volume control."""
import sys
import unittest
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QMouseEvent

from src.app import ClickableSlider, PlayerWindow
from src.library import Library

app = QApplication.instance() or QApplication(sys.argv)


class TestClickableSlider(unittest.TestCase):
    def setUp(self):
        self.slider = ClickableSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 10000)
        self.slider.resize(800, 30)
        self.slider.show()

    def tearDown(self):
        self.slider.close()

    def test_direct_click_jumps_to_coordinate(self):
        """Clicking on the groove must jump the slider value directly to that coordinate."""
        self.assertEqual(self.slider.value(), 0)

        # Simulate left-click near center (x=400)
        press = QMouseEvent(
            QMouseEvent.Type.MouseButtonPress,
            QPointF(400, 15),
            Qt.MouseButton.LeftButton,
            Qt.MouseButton.LeftButton,
            Qt.KeyboardModifier.NoModifier
        )
        self.slider.mousePressEvent(press)

        # Value should jump to ~5000 (within 2% precision of geometry)
        val = self.slider.value()
        self.assertGreater(val, 4800)
        self.assertLess(val, 5200)
        self.assertTrue(self.slider.isSliderDown())

        # Release mouse
        release = QMouseEvent(
            QMouseEvent.Type.MouseButtonRelease,
            QPointF(400, 15),
            Qt.MouseButton.LeftButton,
            Qt.MouseButton.NoButton,
            Qt.KeyboardModifier.NoModifier
        )
        self.slider.mouseReleaseEvent(release)
        self.assertFalse(self.slider.isSliderDown())
        self.assertEqual(self.slider.value(), val)

    def test_smooth_scrubbing_and_signals(self):
        """Dragging the slider should emit sliderMoved with changing values."""
        moved_values = []
        released_values = []
        self.slider.sliderMoved.connect(lambda v: moved_values.append(v))
        self.slider.sliderReleased.connect(lambda: released_values.append(self.slider.value()))

        # Click at 200
        press = QMouseEvent(
            QMouseEvent.Type.MouseButtonPress,
            QPointF(200, 15),
            Qt.MouseButton.LeftButton,
            Qt.MouseButton.LeftButton,
            Qt.KeyboardModifier.NoModifier
        )
        self.slider.mousePressEvent(press)
        self.assertEqual(len(moved_values), 1)

        # Drag to 400
        move1 = QMouseEvent(
            QMouseEvent.Type.MouseMove,
            QPointF(400, 15),
            Qt.MouseButton.NoButton,
            Qt.MouseButton.LeftButton,
            Qt.KeyboardModifier.NoModifier
        )
        self.slider.mouseMoveEvent(move1)
        self.assertGreater(len(moved_values), 1)

        # Drag to 600
        move2 = QMouseEvent(
            QMouseEvent.Type.MouseMove,
            QPointF(600, 15),
            Qt.MouseButton.NoButton,
            Qt.MouseButton.LeftButton,
            Qt.KeyboardModifier.NoModifier
        )
        self.slider.mouseMoveEvent(move2)

        # Release at 600
        release = QMouseEvent(
            QMouseEvent.Type.MouseButtonRelease,
            QPointF(600, 15),
            Qt.MouseButton.LeftButton,
            Qt.MouseButton.NoButton,
            Qt.KeyboardModifier.NoModifier
        )
        self.slider.mouseReleaseEvent(release)

        self.assertEqual(len(released_values), 1)
        self.assertGreater(released_values[0], 7000)
        self.assertFalse(self.slider.isSliderDown())

    def test_clamping_to_boundaries(self):
        """Clicks before the groove or past the groove must clamp to min and max."""
        # Click way to the left (negative x)
        press_left = QMouseEvent(
            QMouseEvent.Type.MouseButtonPress,
            QPointF(-50, 15),
            Qt.MouseButton.LeftButton,
            Qt.MouseButton.LeftButton,
            Qt.KeyboardModifier.NoModifier
        )
        self.slider.mousePressEvent(press_left)
        self.assertEqual(self.slider.value(), 0)

        # Click way to the right (x=2000)
        press_right = QMouseEvent(
            QMouseEvent.Type.MouseButtonPress,
            QPointF(2000, 15),
            Qt.MouseButton.LeftButton,
            Qt.MouseButton.LeftButton,
            Qt.KeyboardModifier.NoModifier
        )
        self.slider.mousePressEvent(press_right)
        self.assertEqual(self.slider.value(), 10000)

    def test_player_window_seek_and_volume_sliders(self):
        """Verify PlayerWindow uses ClickableSlider for seek and volume."""
        import tempfile
        temp = tempfile.TemporaryDirectory()
        try:
            lib = Library(Path(temp.name))
            win = PlayerWindow(lib)
            self.assertIsInstance(win.seek, ClickableSlider)
            self.assertIsInstance(win.volume, ClickableSlider)

            # Test volume slider click jump
            press_vol = QMouseEvent(
                QMouseEvent.Type.MouseButtonPress,
                QPointF(win.volume.width() // 2, win.volume.height() // 2),
                Qt.MouseButton.LeftButton,
                Qt.MouseButton.LeftButton,
                Qt.KeyboardModifier.NoModifier
            )
            win.volume.mousePressEvent(press_vol)
            self.assertGreater(win.volume.value(), 30)
            self.assertLess(win.volume.value(), 70)
            win.close()
        finally:
            temp.cleanup()


if __name__ == '__main__':
    unittest.main()
