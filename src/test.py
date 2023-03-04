from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QTransform, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel

class FlippedLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("color: lightgreen;")

    def paintEvent(self, event):
        painter = QPainter(self)
        transform = QTransform()
        transform.scale(-1, 1)
        transform.translate(-self.width(), 0)
        painter.setTransform(transform)
        painter.drawText(self.rect(), Qt.AlignCenter, self.text())

class BlinkingLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("color: lightgreen;")
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.toggle_visibility)
        self.timer.start(1000)

    def toggle_visibility(self):
        self.setVisible(not self.isVisible())

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 480)
        self.setStyleSheet("background-color: black;")

        self.label1 = FlippedLabel("Flipped Label", self)
        self.label1.setGeometry(50, 50, 200, 50)
        self.label1.show()

        self.label2 = BlinkingLabel("Blinking Label", self)
        self.label2.setGeometry(300, 50, 200, 50)
        self.label2.show()

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
