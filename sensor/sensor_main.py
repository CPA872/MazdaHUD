import board
import brightness_reader
import tempHumidity_reader
import imu_reader
import time

class sensor:

    def __init__(self, dht_pin):
        self.imu = imu_reader.IMUReader()
        self.dht = tempHumidity_reader.TempHumidityReader(dht_pin)
        self.lightSensor = brightness_reader.brightnessReader()
        self.sensor_all_update()

    def imu_update(self):
        self.acceleration = self.imu.get_acceleration() #m/s^2
        self.heading_angle = self.imu.get_heading()[0]
        self.compass_direction = self.imu.get_heading()[1]

    def tempHumidity_update(self):
        self.c_temp = self.dht.get_temperature()[0]
        self.f_temp = self.dht.get_temperature()[1]
        self.humidity = self.dht.get_humidity()
    
    def brightness_update(self):
        self.visible_brightness = self.lightSensor.get_visible()

    def sensor_all_update(self):
        self.imu_update()
        self.tempHumidity_update()
        self.brightness_update()
  