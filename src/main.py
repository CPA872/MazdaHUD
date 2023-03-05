import sys
# import obd
import utils
import hud_widgets
import multiprocessing


from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer


class MazdaHUD(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setFixedSize(800, 480)
        self.setStyleSheet("background-color: black;")

        self.placeholder = QLabel()
        self.setCentralWidget(self.placeholder)

        self.rpm_widget = hud_widgets.RPMWidget()
        self.rpm_widget.move(670, 50)
        self.rpm_widget.setParent(self)
        # self.rpm_widget.move(100, 50)

        self.gps_widget = hud_widgets.GPSWidget()
        self.gps_widget.move(100, 25)
        self.gps_widget.setParent(self)

        self.spd_widget = hud_widgets.SpeedWidget()
        self.spd_widget.move(250, 200)
        self.spd_widget.setParent(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_app = MazdaHUD()
    my_app.show()
    sys.exit(app.exec_())