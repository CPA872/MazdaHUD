import time
import board
import adafruit_dht

class TempHumidityReader:

    def __init__(self, GPIO_pin):
        self.dhtDevice = adafruit_dht.DHT11(GPIO_pin)
        self.error = 0

    def get_c_temperature(self):
        try:
            c_temp = self.dhtDevice.temperature
        except RuntimeError:
            c_temp = -1000.0
        return c_temp
    
    def get_f_temperature(self):
        try:
            f_temp = self.dhtDevice.temperature * 1.8 + 32
        except RuntimeError:
            f_temp = -1000.0
        return f_temp
    
    def get_humidity(self):
        try:
            humidity = self.dhtDevice.humidity
        except RuntimeError:
            humidity = -1000.0
        return humidity
        
    