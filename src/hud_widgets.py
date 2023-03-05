import asyncio
import sys

import obd_reader
import utils
import hud_labels

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QProgressBar, QSizePolicy, QSpacerItem
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QLinearGradient, QColor

from gps_reader import read_gps

class RPMWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(100, 400)
        # self.setStyleSheet("border: 1px solid yellow;")

        self.layout = QVBoxLayout()

        self.rpm_value_label = hud_labels.PlainLabel("4.1", self)
        self.rpm_value_label.setStyleSheet("color: lightgreen; font-size: 15pt; font-family: Consolas;")
        self.layout.addWidget(self.rpm_value_label, alignment=Qt.AlignHCenter)

        self.rpm_bar = QProgressBar()
        self.rpm_bar.setOrientation(Qt.Vertical)
        self.rpm_bar.setTextVisible(False)
        self.rpm_bar.setStyleSheet("background-color: black;")
        self.rpm_bar.setValue(76)
        self.layout.addWidget(self.rpm_bar, alignment=Qt.AlignHCenter)

        self.rpmx1000_label = hud_labels.PlainLabel("RPM \nx1000", self)
        self.rpmx1000_label.setStyleSheet("color: lightgreen; font-size: 12pt; font-family: Consolas;")
        self.layout.addWidget(self.rpmx1000_label, alignment=Qt.AlignHCenter)

        self.rpm_bar.setStyleSheet(
            "QProgressBar { \
                    background-color: black; \
                    border: 1px solid white; \
                } \
             QProgressBar::chunk { \
                background-color: lightgreen; \
                margin: 2px; /* adjust the margin to set the padding */}"
        )

        self.setLayout(self.layout)
        self.update_rpm(0)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_rpm)
        self.timer.start(10)

    def update_rpm(self, rpm=None):
        if rpm is None:
            rpm = utils.obd.get_rpm()
        self.rpm_value_label.setText("%.1f" % (rpm / 1000))
        self.rpm_bar.setValue(int(rpm / 80))
        if rpm < 3500:
            self.rpm_value_label.setStyleSheet("color: lightgreen; font-size: 15pt; font-family: Consolas;")
            self.rpm_bar.setStyleSheet(" QProgressBar::chunk { background-color: lightgreen; }")
        elif rpm < 4500:
            self.rpm_value_label.setStyleSheet("color: orange; font-size: 15pt; font-family: Consolas;")
            self.rpm_bar.setStyleSheet(" QProgressBar::chunk { background-color: orange; }")
        else:
            self.rpm_value_label.setStyleSheet("color: red; font-size: 15pt; font-family: Consolas;")
            self.rpm_bar.setStyleSheet(" QProgressBar::chunk { background-color: red; }")


class GPSWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.setFixedSize(550, 50)
        # self.setStyleSheet("border: 1px solid yellow;")

        self.gps_label = hud_labels.BlinkingBorderedLabel("GPS FIX", utils.LIGHT_GREEN, self)
        self.gps_label.setStyleSheet("color: lightgreen; font-size: 15pt; font-family: Consolas;")

        self.gps_coor_label = hud_labels.PlainLabel(" --.-----° N, --.------° E ", self)
        self.gps_coor_label.setStyleSheet("color: lightgreen; font-size: 15pt; font-family: Consolas;")

        self.gps_alt_label = hud_labels.PlainLabel("ALT ----  ", self)
        self.gps_alt_label.setStyleSheet("color: lightgreen; font-size: 15pt; font-family: Consolas;")

        self.layout.addWidget(self.gps_alt_label)
        self.layout.addWidget(self.gps_coor_label)
        self.layout.addWidget(self.gps_label)

        self.setLayout(self.layout)

        self.gps_timer = QTimer()
        self.gps_timer.timeout.connect(self.update_gps)
        self.gps_timer.start(3000)
        # asyncio.ensure_future(self.update_gps_async())

    def update_gps(self):
        # return
        mode, coor, alt = read_gps()
        print("GPS return: ", mode, coor, alt)
        alt = 120

        if mode == 3:  # GPS 3D FIX
            self.gps_label.stop_blinking()
            self.gps_coor_label.setProperty("text", f" {coor} ")
            self.gps_alt_label.setProperty("text", f" ALT {alt}m")
        else:
            self.gps_label.start_blinking()
            self.gps_label = hud_labels.BlinkingBorderedLabel("GPS FIX", utils.LIGHT_GREEN, self)
            self.gps_label.setStyleSheet("color: lightgreen; font-size: 15pt; font-family: Consolas;")

            self.gps_coor_label = hud_labels.PlainLabel(" --.-----° N, --.------° E ", self)
            self.gps_coor_label.setStyleSheet("color: lightgreen; font-size: 15pt; font-family: Consolas;")

            self.gps_alt_label = hud_labels.PlainLabel("ALT ----  ", self)
            self.gps_alt_label.setStyleSheet("color: lightgreen; font-size: 15pt; font-family: Consolas;")

    # async def update_gps_async(self):
    #     while True:
    #         self.update_gps()
    #         await asyncio.sleep(10)


class SpeedWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(400, 150)
        # self.setStyleSheet("border: 1px solid yellow;")
        self.layout = QHBoxLayout()
        self.mph = True

        self.speed_label = hud_labels.PlainLabel(" 00")
        self.speed_label.setStyleSheet(f"color: {utils.LIGHT_GREEN}; font-size: 120pt; font-family: Consolas;")
        self.speed_label.setAlignment(Qt.AlignRight)

        self.mphkph_label = hud_labels.PlainLabel(" mph")
        self.mphkph_label.setStyleSheet(f"color: {utils.LIGHT_GREEN}; font-size: 20pt; font-family: Consolas;")
        self.layout.addWidget(self.mphkph_label, alignment=Qt.AlignBottom)
        self.layout.addWidget(self.speed_label)

        self.setLayout(self.layout)

        self.update_speed(75, 120)
        self.update_format(False)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_speed)
        self.timer.start(10)

    def update_speed(self, spd_kph=None, spd_mph=None):
        spd_kph, spd_mph = utils.obd.get_speed()

        if self.mph:
            self.speed_label.setText("%3d" % int(spd_mph))
        else:
            self.speed_label.setText("%3d" % int(spd_kph))
        self.speed_label.setStyleSheet(f"color: {utils.LIGHT_GREEN}; font-size: 120pt; font-family: Consolas;")

    def update_format(self, mph):
        if mph:
            self.mph = True
            self.mphkph_label.setProperty("text", " mph")
        else:
            self.mph = False
            self.mphkph_label.setProperty("text", " kph")


class BottomStatusWidget(QWidget):
    def __init__(self):
        super().__init__()
