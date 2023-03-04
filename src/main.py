import sys
# import obd
import utils
import hud_labels

from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget

from rpm_bar import RPMBar

class MazdaHUD(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setFixedSize(800, 480)
        self.setStyleSheet("background-color: black;")
        self.layout = QVBoxLayout()
        
        self.rpm_value_label = hud_labels.PlainLabel("4.1", 50, 50, self)
        self.rpm_value_label.setStyleSheet("color: lightgreen; font-size: 20pt;")
        self.rpm_value_label.move(50, 50)

        self.rpmx1000_label = hud_labels.PlainLabel("RPM x1000", 50, 50)
        
        self.gps_label = hud_labels.BlinkingBorderedLabel("GPS", 200, 50, utils.LIGHT_GREEN)

        self.gps_spd_label = hud_labels.PlainLabel("SPD ---", 250, 50)

        self.gps_alt_label = hud_labels.PlainLabel("ALT ---", 400, 50)
            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_app = MazdaHUD()
    my_app.show()
    sys.exit(app.exec_())