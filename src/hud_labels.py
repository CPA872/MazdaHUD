from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QTransform
from PyQt5.QtWidgets import QLabel

# label with text horizontally flipped.
class FlippedLabel(QLabel):

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        # self.setStyleSheet(f"color: {utils.LIGHT_GREEN}")
        # self.setStyleSheet(f"font {utils.SMALL_FONT_SIZE}pt {utils.DEFAUT_FONT}")
        # self.setAlignment(Qt.AlignLeft)

    def paintEvent(self, event):
        painter = QPainter(self)
        transform = QTransform()
        transform.scale(-1, 1)
        transform.translate(-self.width(), 0)
        painter.setTransform(transform)
        painter.drawText(self.rect(), Qt.AlignCenter, self.text())


class PlainLabel(FlippedLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("background-color: black;")


class BorderedLabel(FlippedLabel):
    def __init__(self, text, border_color, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("background-color: black;")
        self.setStyleSheet(f"border: 2px solid {border_color}; padding: 5px;")


class BlinkingLabel(FlippedLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("padding: 5px;")
        self.timer = QTimer()
        self.timer.timeout.connect(self.toggle_visibility)
        self.timer.start(1000)
        self.visible = True

    def toggle_visibility(self):
        self.visible = not self.visible
        self.setVisible(self.visible)


class BlinkingBorderedLabel(FlippedLabel):
    def __init__(self, text, border_color, parent=None):
        super().__init__(text, parent)
        self.border_color = border_color
        self.setStyleSheet(f" border: 1px solid {border_color}; padding: 5px;")

        self.timer = QTimer()
        self.timer.timeout.connect(self.toggle_border)
        self.timer.start(1000)  # blink every second

        self.border_visible = True

    def toggle_border(self):
        self.border_visible = not self.border_visible
        border_style = f"1px solid {self.border_color}" if self.border_visible else "0px"
        self.setStyleSheet(
            f"color: {self.border_color}; font-size: 15pt; font-family: Consolas; border: {border_style}; padding: 5px;")

    def stop_blinking(self):
        self.timer.stop()
        self.border_visible = True
        border_style = f"2px solid {self.border_color}" if self.border_visible else "0px"
        self.setStyleSheet(
            f"color: {self.border_color}; font-size: 15pt; font-family: Consolas; border: {border_style}; padding: 5px;")

    def start_blinking(self):
        self.timer.start()