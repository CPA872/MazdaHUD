import utils
import hud_labels

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QProgressBar, QSizePolicy, QSpacerItem
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QLinearGradient, QColor


class RPMWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(100, 400)
        # self.setStyleSheet("border: 1px solid yellow;")

        self.layout = QVBoxLayout()

        self.rpm_value_label = hud_labels.PlainLabel("4100", self)
        self.rpm_value_label.setStyleSheet(f"color: {utils.DISPLAY_COLORS[utils.curr_color]}; font-size: 15pt; font-family: Consolas;")
        self.layout.addWidget(self.rpm_value_label, alignment=Qt.AlignHCenter)

        self.rpm_bar = QProgressBar()
        self.rpm_bar.setOrientation(Qt.Vertical)
        self.rpm_bar.setTextVisible(False)
        self.rpm_bar.setStyleSheet("background-color: black;")
        self.rpm_bar.setValue(76)
        self.layout.addWidget(self.rpm_bar, alignment=Qt.AlignHCenter)

        self.rpmx1000_label = hud_labels.PlainLabel("RPM \nx1000", self)
        self.rpmx1000_label.setStyleSheet(f"color: {utils.DISPLAY_COLORS[utils.curr_color]}; font-size: 15pt; font-family: Consolas;")
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
        self.rpm_value_label.setText(f"{int(rpm / 10 * 10):4}")
        self.rpm_bar.setValue(int(rpm / 80))
        if rpm < 3000:
            self.rpm_value_label.setStyleSheet("color: lightgreen; font-size: 20pt; font-family: Consolas;")
            self.rpm_bar.setStyleSheet(" QProgressBar::chunk { background-color: lightgreen; }")
        elif rpm < 4500:
            self.rpm_value_label.setStyleSheet("color: orange; font-size: 20pt; font-family: Consolas;")
            self.rpm_bar.setStyleSheet(" QProgressBar::chunk { background-color: orange; }")
        else:
            self.rpm_value_label.setStyleSheet("color: red; font-size: 20pt; font-family: Consolas;")
            self.rpm_bar.setStyleSheet(" QProgressBar::chunk { background-color: red; }")
        
        self.rpmx1000_label.setStyleSheet(f"color: {utils.DISPLAY_COLORS[utils.curr_color]}; font-size: 15pt; font-family: Consolas;")
        
        if utils.DISPLAY_MODES[utils.curr_mode] in ["zen_metric", "zen_imperial"]:
            self.setVisible(False)
        else:
            self.setVisible(True)


class GPSWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.setFixedSize(550, 50)
        # self.setStyleSheet("border: 1px solid yellow;")

        self.gps_label = hud_labels.BlinkingBorderedLabel("GPS FIX", utils.DISPLAY_COLORS[utils.curr_color], self)
        self.gps_label.setStyleSheet(f"color: {utils.DISPLAY_COLORS[utils.curr_color]}; font-size: 15pt; font-family: Consolas;")

        self.gps_coor_label = hud_labels.PlainLabel(" --.-----° N, --.------° E ", self)
        self.gps_coor_label.setStyleSheet(f"color: {utils.DISPLAY_COLORS[utils.curr_color]}; font-size: 15pt; font-family: Consolas;")

        self.gps_alt_label = hud_labels.PlainLabel("ALT ---- ", self)
        self.gps_alt_label.setStyleSheet(f"color: {utils.DISPLAY_COLORS[utils.curr_color]}; font-size: 15pt; font-family: Consolas;")
        self.gps_alt_label.setVisible(False)

        self.layout.addWidget(self.gps_alt_label)
        self.layout.addWidget(self.gps_coor_label)
        self.layout.addWidget(self.gps_label)

        self.setLayout(self.layout)

        self.gps_timer = QTimer()
        self.gps_timer.timeout.connect(self.update_gps)
        self.gps_timer.start(1000)
        # asyncio.ensure_future(self.update_gps_async())
        
    def update_gps(self):
        # print("call update_gps in gps widget, mode ", utils.gps_reader.mode)
        if utils.gps_reader.mode == 3:  # GPS 3D FIX
            self.gps_coor_label.setProperty("text", f" {utils.gps_reader.coor} ")
            self.gps_alt_label.setProperty("text", f" ALT {utils.gps_reader.alt}m")
            
            self.gps_alt_label.setStyleSheet(f"color: {utils.DISPLAY_COLORS[utils.curr_color]}; font-size: 15pt; font-family: Consolas;")
            self.gps_coor_label.setStyleSheet(f"color: {utils.DISPLAY_COLORS[utils.curr_color]}; font-size: 15pt; font-family: Consolas;")
            self.gps_label.setStyleSheet(f"color: {utils.DISPLAY_COLORS[utils.curr_color]}; font-size: 15pt; font-family: Consolas;")
            self.gps_label.stop_blinking()
        else:
            # self.gps_label = hud_labels.BlinkingBorderedLabel(f"GPS FIX", {utils.DISPLAY_COLORS[utils.curr_color]}, self)
            self.gps_label.setStyleSheet(f"color: {utils.DISPLAY_COLORS[utils.curr_color]}; font-size: 15pt; font-family: Consolas;")

            self.gps_coor_label.setText(" --.-----° N, --.------° E ")
            self.gps_coor_label.setStyleSheet(f"color: {utils.DISPLAY_COLORS[utils.curr_color]}; font-size: 15pt; font-family: Consolas;")

            self.gps_alt_label.setText("ALT ---- ")
            self.gps_alt_label.setStyleSheet(f"color: {utils.DISPLAY_COLORS[utils.curr_color]}; font-size: 15pt; font-family: Consolas;")
            self.gps_label.start_blinking()
        
        if utils.DISPLAY_MODES[utils.curr_mode] in ["zen_metric", "zen_imperial"]:
            self.setVisible(False)
        else:
            self.setVisible(True)
           

class SpeedWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(450, 150)
        # self.setStyleSheet("border: 1px solid yellow;")
        self.layout = QHBoxLayout()
        self.mph = True

        self.speed_label = hud_labels.PlainLabel("00 ")
        self.speed_label.setStyleSheet(f"color: {utils.DISPLAY_COLORS[utils.curr_color]}; font-size: 120pt; font-family: Cascadia Mono Light 300;")
        self.speed_label.setAlignment(Qt.AlignRight)

        self.mphkph_label = hud_labels.PlainLabel("mph")
        self.mphkph_label.setStyleSheet(f"color: {utils.DISPLAY_COLORS[utils.curr_color]}; font-size: 20pt; font-family: Consolas;")
        self.layout.addWidget(self.mphkph_label, alignment=Qt.AlignBottom)
        self.layout.addWidget(self.speed_label)

        self.setLayout(self.layout)

        self.update_speed(75, 120)
        self.update_format(mph=True)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_speed)
        self.timer.start(10)

    def update_speed(self, spd_mph=None, spd_kph=None):
        spd_mph, spd_kph = utils.obd.get_speed()

        if self.mph:
            self.speed_label.setText("%3d" % int(spd_mph))
        else:
            self.speed_label.setText("%3d" % int(spd_kph))
            
        self.speed_label.setStyleSheet(f"color: {utils.DISPLAY_COLORS[utils.curr_color]}; font-size: 120pt; font-family: Consolas;")
        self.mphkph_label.setStyleSheet(f"color: {utils.DISPLAY_COLORS[utils.curr_color]}; font-size: 20pt; font-family: Consolas;")
        
        if utils.DISPLAY_MODES[utils.curr_mode] in ["normal_imperial", "zen_imperial", "full_imperial"]:
            self.update_format(True)
        else:
            self.update_format(False)

    def update_format(self, mph):
        if mph:
            self.mph = True
            self.mphkph_label.setProperty("text", "mph")
        else:
            self.mph = False
            self.mphkph_label.setProperty("text", "kph")


class StatusWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setFixedSize(150, 250)
        
        self.hdg_label     = hud_labels.PlainLabel("HDG --- °")
        self.hdg_label.setStyleSheet(f"color: {utils.DISPLAY_COLORS[utils.curr_color]}; font-size: 15pt; font-family: Consolas;")
        self.layout.addWidget(self.hdg_label, alignment=Qt.AlignRight)
        
        self.dir_label     = hud_labels.PlainLabel("DIR --")
        self.dir_label.setStyleSheet(f"color: {utils.DISPLAY_COLORS[utils.curr_color]}; font-size: 15pt; font-family: Consolas;")
        self.layout.addWidget(self.dir_label, alignment=Qt.AlignRight)
        
        self.coolant_label = hud_labels.PlainLabel("ECT --- °C")
        self.coolant_label.setStyleSheet(f"color: {utils.DISPLAY_COLORS[utils.curr_color]}; font-size: 15pt; font-family: Consolas;")
        self.layout.addWidget(self.coolant_label, alignment=Qt.AlignRight)
        
        self.iat_label     = hud_labels.PlainLabel("IAT ---- °C")
        self.iat_label.setStyleSheet(f"color: {utils.DISPLAY_COLORS[utils.curr_color]}; font-size: 15pt; font-family: Consolas;")
        self.layout.addWidget(self.iat_label, alignment=Qt.AlignRight)
        
        self.acc_label     = hud_labels.PlainLabel("ACC ---")
        self.acc_label.setStyleSheet(f"color: {utils.DISPLAY_COLORS[utils.curr_color]}; font-size: 15pt; font-family: Consolas;")
        self.layout.addWidget(self.acc_label, alignment=Qt.AlignRight)
        
        self.mode_label     = hud_labels.PlainLabel("------")
        self.mode_label.setStyleSheet(f"color: {utils.DISPLAY_COLORS[utils.curr_color]}; font-size: 15pt; font-family: Consolas;")
        self.layout.addWidget(self.mode_label, alignment=Qt.AlignRight)

        # self.status_label = hud_labels.PlainLabel("[test]")
        # self.layout.addWidget(self.status_label)
        # self.status_label.setStyleSheet(f"color: {utils.DISPLAY_COLORS[utils.curr_color]}; font-size: 15pt; font-family: Consolas;")
        # self.status_label.setProperty("text", f"acc: {utils.sensor_reader.acceleration:2f}, temp: {utils.sensor_reader.c_temp}, hdg: {utils.sensor_reader.heading_angle}")

        self.setLayout(self.layout)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_sensors)
        self.timer.start(100)
        
    def update_sensors(self):
        # print("called update sensors")
        # utils.sensor_reader.sensor_all_update()
        # self.status_label.setProperty("text", f"ACC: {utils.sensor_reader.acceleration:.2f} IAT: {utils.sensor_reader.c_temp:.1f} °C, HDG: {utils.sensor_reader.heading_angle:.0f}")
        self.coolant_label.setProperty("text", f"ECT {utils.obd.get_coolant_temp()}")
        iat = utils.sensor_reader.c_temp
        if (iat < 80 and iat > -20):
            self.iat_label.setProperty("text", f"IAT {iat}")
            
        self.hdg_label.setProperty("text", f"HDG {int(utils.sensor_reader.heading_angle):03}")
        self.dir_label.setProperty("text", f"DIR {utils.sensor_reader.compass_direction}")
        self.acc_label.setProperty("text", f"ACC {utils.sensor_reader.acceleration:.2f}")

        # print("==== brightness: ", utils.sensor_reader.brightness)
        
        if utils.DISPLAY_MODES[utils.curr_mode] in ["full_metric", "full_imperial"]:
            self.hdg_label.setVisible(True)
            self.dir_label.setVisible(True)
            self.acc_label.setVisible(True)
            self.iat_label.setVisible(True)
            self.coolant_label.setVisible(True)
            
        else:
            self.hdg_label.setVisible(False)
            self.dir_label.setVisible(False)
            self.acc_label.setVisible(False)
            self.iat_label.setVisible(False)
            self.coolant_label.setVisible(False)
        
        if utils.sensor_reader.button_pressed == True: 
            utils.curr_mode = (utils.curr_mode + 1) % 6
            utils.sensor_reader.button_pressed = False
            
               # print(f"mode {utils.curr_mode} color {utils.curr_color}")
        if utils.sensor_reader.brightness > 900000:
            utils.curr_color = 0
        else:
            utils.curr_color = 1
        
        self.hdg_label.setStyleSheet(f"color: {utils.DISPLAY_COLORS[utils.curr_color]}; font-size: 15pt; font-family: Consolas;")
        self.dir_label.setStyleSheet(f"color: {utils.DISPLAY_COLORS[utils.curr_color]}; font-size: 15pt; font-family: Consolas;")
        self.acc_label.setStyleSheet(f"color: {utils.DISPLAY_COLORS[utils.curr_color]}; font-size: 15pt; font-family: Consolas;")
        self.iat_label.setStyleSheet(f"color: {utils.DISPLAY_COLORS[utils.curr_color]}; font-size: 15pt; font-family: Consolas;")
        self.coolant_label.setStyleSheet(f"color: {utils.DISPLAY_COLORS[utils.curr_color]}; font-size: 15pt; font-family: Consolas;")
        self.mode_label.setStyleSheet(f"color: {utils.DISPLAY_COLORS[utils.curr_color]}; font-size: 15pt; font-family: Consolas;")
        self.mode_label.setProperty("text", "-" * utils.curr_mode + "*" + "-" * (6 - utils.curr_mode - 1))
