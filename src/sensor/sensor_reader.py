from PyQt5.QtCore import QRunnable, QThread

import board
import brightness_reader
import tempHumidity_reader
import imu_reader
import time

import RPi.GPIO as GPIO

BUTTON_GPIO = 15

class SensorReader(QThread):
    def __init__(self, dht_pin):
        super().__init__()
        self.imu = imu_reader.IMUReader()
        self.dht = tempHumidity_reader.TempHumidityReader(dht_pin)
        self.lightSensor = brightness_reader.brightnessReader()
        # self.sensor_all_update()
        self.button_pressed = False
        
        self.acceleration = 0
        self.heading_angle = 0
        self.compass_direction = 0
        
        self.c_temp = 0
        self.f_temp = 0
        self.humidity = 0
        
        self.brightness = 0
        
        self.stopped = False
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(BUTTON_GPIO, GPIO.FALLING, 
            callback=self.button_pressed_callback, bouncetime=200)

    def button_pressed_callback(self, channel):
        print("button presses")
        self.button_pressed = True

    def imu_update(self):
        self.acceleration = self.imu.get_acceleration() #m/s^2
        self.heading_angle = self.imu.get_heading()[0]
        self.compass_direction = self.imu.get_heading()[1]

    def tempHumidity_update(self):
        self.c_temp = self.dht.get_temperature()[0]
        self.f_temp = self.dht.get_temperature()[1]
        self.humidity = self.dht.get_humidity()
    
    def brightness_update(self):
        self.brightness = self.lightSensor.get_visible()

    def sensor_all_update(self):
        self.imu_update()
        self.tempHumidity_update()
        self.brightness_update()
        
    def run(self):
        while not self.stopped:
            if self.isInterruptionRequested():
                return
            
            # print("update loop")
            self.sensor_all_update()
            time.sleep(0.05)
  
    def stop(self):
        self.stopped = True
        
    