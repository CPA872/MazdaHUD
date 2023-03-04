import sys
import utils
import hud_labels

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QProgressBar, QSizePolicy, QSpacerItem
from PyQt5.QtWidgets import QWidget


class RPMWidget(QWidget):
    def __init__(self):
        super().__init__()
        # self.setGeometry(50, 50, 50, 400)
        # self.move(100, 50)
        self.setFixedSize(100, 400)
        # self.setStyleSheet("border: 1px solid yellow;")

        self.layout = QVBoxLayout()
        self.layout.addItem(QSpacerItem(10, 20, QSizePolicy.Minimum))
        # self.rpm_layout.setAlignment(Qt.AlignCenter)
        # self.rpm_layout.setAlignment(Qt.AlignHCenter)

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

        self.setLayout(self.layout)

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
        self.layout = QHBoxLayout()
        self.setFixedSize(400, 50)
        # self.setStyleSheet("border: 1px solid yellow;")

        self.gps_label = hud_labels.BlinkingBorderedLabel("GPS", utils.LIGHT_GREEN, self)
        self.gps_label.setStyleSheet("color: lightgreen; font-size: 15pt; font-family: Consolas;")
        self.layout.addWidget(self.gps_label)

        self.gps_spd_label = hud_labels.PlainLabel("  SPD ---  ", self)
        self.gps_spd_label.setStyleSheet("color: lightgreen; font-size: 15pt; font-family: Consolas;")
        self.layout.addWidget(self.gps_spd_label)

        self.gps_alt_label = hud_labels.PlainLabel("  ALT ----  ", self)
        self.gps_alt_label.setStyleSheet("color: lightgreen; font-size: 15pt; font-family: Consolas;")
        self.layout.addWidget(self.gps_alt_label)

        self.setLayout(self.layout)

    def update_gps(self, fix_state, spd, alt):
        if fix_state:
            self.gps_label.stop_blinking()
        if not fix_state:
            self.gps_label.start_blinking()
            self.gps_spd_label.setText("  SPD ---  ")
            self.gps_alt_label.setText("  ALT ----  ")

        self.gps_spd_label.setText("  SPD %3d" % int(spd))
        self.gps_alt_label.setText("  ALT %4d" % int(alt))