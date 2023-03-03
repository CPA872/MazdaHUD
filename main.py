# This Python file uses the following encoding: utf-8
import sys
import obd
import asyncio

from PySide6 import QtCore
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

class HUD(QMainWindow):
    def __init__(self):
        super().__init__()

        self.loader = QUiLoader()
        self.ui = self.loader.load("hud1.ui")
        self.ui.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.modes = [
            "zen",     # speed only
            "normal",  # speed rpm coolant
            "full",    # speed rpm coolant gps indoor-temp
            "gps"      # gps data
        ]

        self.mode_select = 0
        self.label_speed        = self.ui.label_speed
        self.label_mph_kph      = self.ui.label_mph_kph
        self.label_speed        = None
        self.label_rpm          = None
        self.label_coolant_temp = None
        self.label_gps_fix      = None
        self.label_gps_long     = None
        self.label_gps_lat      = None
        self.label_gps_speed    = None
        self.label_gps_alt      = None
        self.label_indoor_temp  = None
        self.label_indoor_humd  = None
        self.label_x_accel      = None
        self.label_y_accel      = None
        self.label_z_accel      = None

        # from OBDII
        self.speed = 0
        self.rpm   = 0
        self.coolant_temp = 0

        # from other sensors
        self.indoor_temp = 0
        self.indoor_humd = 0
        self.x_accel = 0
        self.y_accel = 0
        self.z_accel = 0

        # from GPS
        self.gps_fix = False
        self.gps_lat = 0
        self.gps_long = 0
        self.gps_speed = 0
        self.gps_alt = 0


    # This functions resets the labels fields
    # to make sure that we update the correct UI elements
    def change_ui(self):
        pass

    def update_speed(self):
        pass

    def update_gps(self):
        pass

    def update_temp_sensor(self):
        pass

    def update_gyro(self):
        pass

def main():
    app = QApplication(sys.argv)
    main_window = HUD()

    main_window.ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

