import sys
import utils
import hud_labels

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QProgressBar
from PyQt5.QtWidgets import QWidget


class RPMWidget(QWidget):
    def __init__(self):
        super().__init__()
        # self.setGeometry(50, 50, 50, 400)
        self.setFixedSize(150, 400)
        # self.setStyleSheet("border: 1px solid yellow;")

        self.rpm_layout = QVBoxLayout()
        # self.rpm_layout.setAlignment(Qt.AlignCenter)
        # self.rpm_layout.setAlignment(Qt.AlignHCenter)

        self.rpm_value_label = hud_labels.PlainLabel("4.1", self)
        self.rpm_value_label.setStyleSheet("color: lightgreen; font-size: 15pt; font-family: Consolas;")
        self.rpm_layout.addWidget(self.rpm_value_label)

        self.rpm_bar = QProgressBar()
        self.rpm_bar.setOrientation(Qt.Vertical)
        self.rpm_bar.setTextVisible(False)
        self.rpm_bar.setStyleSheet("background-color: black;")
        self.rpm_bar.setValue(76)
        self.rpm_layout.addWidget(self.rpm_bar, alignment=Qt.AlignHCenter)

        self.rpmx1000_label = hud_labels.PlainLabel("RPM \nx1000", self)
        self.rpmx1000_label.setStyleSheet("color: lightgreen; font-size: 10pt; font-family: Consolas;")
        self.rpm_layout.addWidget(self.rpmx1000_label)

        self.setLayout(self.rpm_layout)

        self.update_rpm(4000)

    def update_rpm(self, rpm):
        self.rpm_value_label.setText("%.1f" % (rpm / 1000))
        self.rpm_bar.setValue(int(rpm / 80))
        if rpm < 3500:
            self.rpm_value_label.setStyleSheet("color: lightgreen; font-size: 15pt; font-family: Consolas;")
            self.rpm_bar.setStyleSheet(
                "QProgressBar { \
                        background-color: black; \
                        border: 1px solid white; \
                    } \
                QProgressBar::chunk { \
                background-color: lightgreen; \
                margin: 2px; /* adjust the margin to set the padding */}"
                )
        elif rpm < 4500:
            self.rpm_value_label.setStyleSheet("color: orange; font-size: 15pt; font-family: Consolas;")
            self.rpm_bar.setStyleSheet(
                "QProgressBar { \
                        background-color: black; \
                        border: 1px solid white; \
                    } \
                QProgressBar::chunk { \
                background-color: orange; \
                margin: 2px; /* adjust the margin to set the padding */}"
            )
        else:
            self.rpm_value_label.setStyleSheet("color: red; font-size: 15pt; font-family: Consolas;")
            self.rpm_bar.setStyleSheet(
                "QProgressBar { \
                        background-color: black; \
                        border: 1px solid white; \
                    } \
                QProgressBar::chunk { \
                background-color: red; \
                margin: 2px; /* adjust the margin to set the padding */}"
            )


class GPSWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.gps_label = hud_labels.BlinkingBorderedLabel("GPS", utils.LIGHT_GREEN, self)

        self.gps_spd_label = hud_labels.PlainLabel("SPD ---", self)

        self.gps_alt_label = hud_labels.PlainLabel("ALT ---", self)