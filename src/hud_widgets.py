import utils
import hud_labels

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QProgressBar, QSizePolicy, QSpacerItem
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QLinearGradient, QColor

button_pressed = False
display_modes = ["normal_metric", "normal_imperial", "zen_metric", "zen_imperial", "full_metric", "full_imperial"]
current_mode = 0
DAY_GREEN = "#33FF00"
NIGHT_AMBER = "#FFC000"
curr_color = NIGHT_AMBER


class RPMWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(100, 400)
        # self.setStyleSheet("border: 1px solid yellow;")

        self.layout = QVBoxLayout()

        self.rpm_value_label = hud_labels.PlainLabel("4100", self)
        self.rpm_value_label.setStyleSheet(f"color: {curr_color}; font-size: 15pt; font-family: Consolas;")
        self.layout.addWidget(self.rpm_value_label, alignment=Qt.AlignHCenter)

        self.rpm_bar = QProgressBar()
        self.rpm_bar.setOrientation(Qt.Vertical)
        self.rpm_bar.setTextVisible(False)
        self.rpm_bar.setStyleSheet("background-color: black;")
        self.rpm_bar.setValue(76)
        self.layout.addWidget(self.rpm_bar, alignment=Qt.AlignHCenter)

        self.rpmx1000_label = hud_labels.PlainLabel("RPM \nx1000", self)
        self.rpmx1000_label.setStyleSheet(f"color: {curr_color}; font-size: 12pt; font-family: Consolas;")
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
        
        global button_pressed
        if button_pressed == True:
            self.setVisible(False)
            button_pressed = False
        
    # def update_color(self):
    #     if 


class GPSWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.setFixedSize(550, 50)
        # self.setStyleSheet("border: 1px solid yellow;")

        self.gps_label = hud_labels.BlinkingBorderedLabel("GPS FIX", curr_color, self)
        self.gps_label.setStyleSheet(f"color: {curr_color}; font-size: 15pt; font-family: Consolas;")

        self.gps_coor_label = hud_labels.PlainLabel(" --.-----° N, --.------° E ", self)
        self.gps_coor_label.setStyleSheet(f"color: {curr_color}; font-size: 15pt; font-family: Consolas;")

        self.gps_alt_label = hud_labels.PlainLabel("ALT ---- ", self)
        self.gps_alt_label.setStyleSheet(f"color: {curr_color}; font-size: 15pt; font-family: Consolas;")

        self.layout.addWidget(self.gps_alt_label)
        self.layout.addWidget(self.gps_coor_label)
        self.layout.addWidget(self.gps_label)

        self.setLayout(self.layout)

        self.gps_timer = QTimer()
        self.gps_timer.timeout.connect(self.update_gps)
        self.gps_timer.start(3000)
        # asyncio.ensure_future(self.update_gps_async())

    def update_gps(self):
        print("call update_gps in gps widget, mode ", utils.gps_reader.mode)
        if utils.gps_reader.mode == 3:  # GPS 3D FIX
            self.gps_label.stop_blinking()
            self.gps_coor_label.setProperty("text", f" {utils.gps_reader.coor} ")
            self.gps_alt_label.setProperty("text", f" ALT {utils.gps_reader.alt}m")
        else:
            self.gps_label.start_blinking()
            self.gps_label = hud_labels.BlinkingBorderedLabel(f"GPS FIX", {curr_color}, self)
            self.gps_label.setStyleSheet(f"color: {curr_color}; font-size: 15pt; font-family: Consolas;")

            self.gps_coor_label = hud_labels.PlainLabel(" --.-----° N, --.------° E ", self)
            self.gps_coor_label.setStyleSheet(f"color: {curr_color}; font-size: 15pt; font-family: Consolas;")

            self.gps_alt_label = hud_labels.PlainLabel("ALT ---- ", self)
            self.gps_alt_label.setStyleSheet(f"color: {curr_color}; font-size: 15pt; font-family: Consolas;")
        

class SpeedWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(450, 150)
        # self.setStyleSheet("border: 1px solid yellow;")
        self.layout = QHBoxLayout()
        self.mph = True

        self.speed_label = hud_labels.PlainLabel("00 ")
        self.speed_label.setStyleSheet(f"color: {curr_color}; font-size: 120pt; font-family: Consolas;")
        self.speed_label.setAlignment(Qt.AlignRight)

        self.mphkph_label = hud_labels.PlainLabel("mph")
        self.mphkph_label.setStyleSheet(f"color: {curr_color}; font-size: 20pt; font-family: Consolas;")
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
        self.speed_label.setStyleSheet(f"color: {curr_color}; font-size: 120pt; font-family: Consolas;")

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


class StatusWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setFixedSize(150, 250)
        
        self.hdg_label     = hud_labels.PlainLabel("HDG --- °")
        self.hdg_label.setStyleSheet(f"color: {curr_color}; font-size: 15pt; font-family: Consolas;")
        self.layout.addWidget(self.hdg_label, alignment=Qt.AlignRight)
        
        self.dir_label     = hud_labels.PlainLabel("DIR --")
        self.dir_label.setStyleSheet(f"color: {curr_color}; font-size: 15pt; font-family: Consolas;")
        self.layout.addWidget(self.dir_label, alignment=Qt.AlignRight)
        
        self.coolant_label = hud_labels.PlainLabel("ECT --- °C")
        self.coolant_label.setStyleSheet(f"color: {curr_color}; font-size: 15pt; font-family: Consolas;")
        self.layout.addWidget(self.coolant_label, alignment=Qt.AlignRight)
        
        self.iat_label     = hud_labels.PlainLabel("IAT ---- °C")
        self.iat_label.setStyleSheet(f"color: {curr_color}; font-size: 15pt; font-family: Consolas;")
        self.layout.addWidget(self.iat_label, alignment=Qt.AlignRight)
        
        self.acc_label     = hud_labels.PlainLabel("ACC ---")
        self.acc_label.setStyleSheet(f"color: {curr_color}; font-size: 15pt; font-family: Consolas;")
        self.layout.addWidget(self.acc_label, alignment=Qt.AlignRight)

        # self.status_label = hud_labels.PlainLabel("[test]")
        # self.layout.addWidget(self.status_label)
        # self.status_label.setStyleSheet(f"color: {curr_color}; font-size: 15pt; font-family: Consolas;")
        # self.status_label.setProperty("text", f"acc: {utils.sensor_reader.acceleration:2f}, temp: {utils.sensor_reader.c_temp}, hdg: {utils.sensor_reader.heading_angle}")

        self.setLayout(self.layout)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_sensors)
        self.timer.start(50)
        
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
        
        global current_mode
        if utils.sensor_reader.button_pressed == True: 
            current_mode = (current_mode + 1) % 6
            utils.sensor_reader.button_pressed = False
            
            
class HeadingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        