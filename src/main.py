import sys
# import obd
import utils
import hud_labels
import hud_widgets

from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QProgressBar
from PyQt5.QtWidgets import QWidget

from rpm_bar import RPMBar

class MazdaHUD(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setFixedSize(800, 480)
        self.setStyleSheet("background-color: black;")

        self.rpm_widget = hud_widgets.RPMWidget()
        self.setCentralWidget(self.rpm_widget)
        # self.rpm_widget.move(100, 50)

        self.gps_widget = hud_widgets.GPSWidget()
        self.gps_widget.move(200, 25)
        self.gps_widget.setParent(self)

        self.spd_widget = hud_widgets.SpeedWidget()
        self.spd_widget.move(150, 200)
        self.spd_widget.setParent(self)
        # self.layout = QVBoxLayout()
        # self.layout.addWidget(self.rpm_widget)

        # central_widget = QWidget(self)
        # central_widget.setLayout(self.layout)
        # self.setCentralWidget(central_widget)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_app = MazdaHUD()
    my_app.show()
    sys.exit(app.exec_())