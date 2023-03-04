import sys
import utils
import hud_labels

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QProgressBar, QSizePolicy, QSpacerItem
from PyQt5.QtWidgets import QWidget


class RPMWidget(QWidget):
    def __init__(self):
        super().__init__()
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

        self.gps_spd_label = hud_labels.PlainLabel("  SPD ---  ", self)
        self.gps_spd_label.setStyleSheet("color: lightgreen; font-size: 15pt; font-family: Consolas;")

        self.gps_alt_label = hud_labels.PlainLabel("  ALT ----  ", self)
        self.gps_alt_label.setStyleSheet("color: lightgreen; font-size: 15pt; font-family: Consolas;")

        self.layout.addWidget(self.gps_alt_label)
        self.layout.addWidget(self.gps_spd_label)
        self.layout.addWidget(self.gps_label)

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


class SpeedWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(400, 150)
        self.setStyleSheet("border: 1px solid yellow;")
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

    def update_speed(self, spd_mph, spd_kph):
        if self.mph:
            self.speed_label.setText("%3d" % int(spd_mph))
        else:
            self.speed_label.setText("%3d" % int(spd_kph))
        self.speed_label.setStyleSheet(f"color: {utils.LIGHT_GREEN}; font-size: 120pt; font-family: Consolas;")

    def update_format(self, mph):
        if mph:
            self.mph = True
            self.mphkph_label.setText(" mph")
            self.mphkph_label.setStyleSheet(f"color: {utils.LIGHT_GREEN}; font-size: 20pt; font-family: Consolas;")
        else:
            self.mph = False
            self.mphkph_label.setText(" kph")
            self.mphkph_label.setStyleSheet(f"color: {utils.LIGHT_GREEN}; font-size: 20pt; font-family: Consolas;")