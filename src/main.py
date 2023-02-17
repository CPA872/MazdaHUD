import sys
import utils
import hud_widgets
import multiprocessing

from PyQt5 import QtCore
from PyQt5.QtCore import QObject, QRunnable, QThreadPool
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
        self.gps_widget.move(100, 50)
        self.gps_widget.setParent(self)

        self.spd_widget = hud_widgets.SpeedWidget()
        self.spd_widget.move(200, 200)
        self.spd_widget.setParent(self)
        
        self.status_widget = hud_widgets.StatusWidget()
        self.status_widget.move(50, 125)
        self.status_widget.setParent(self)
        
        self.thread_pool = QThreadPool.globalInstance()
        self.thread_pool.setMaxThreadCount(2) 

        utils.sensor_reader.start()
        utils.gps_reader.start()

        # self.thread_pool.start(utils.sensor_reader)
        # self.thread_pool.start(utils.gps_reader)
        
        
    def closeEvent(self, event):
        # Stop the threads before closing the window
        self.thread_pool.clear()
        super().closeEvent(event)
        

if __name__ == '__main__':
    # sensor_process = multiprocessing.Process(target=utils.sensors.update_loop)
    # sensor_process.start()
    
    app = QApplication(sys.argv)
    my_app = MazdaHUD()
    my_app.show()
    # app.aboutToQuit.connect(my_app.thread_pool.waitForDone)

    sys.exit(app.exec_())
    
"""
    TODO: thread not stop after main app quit
    TODO: GPS thread update
"""