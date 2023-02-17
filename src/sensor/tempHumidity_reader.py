import time
import board
import adafruit_dht

class TempHumidityReader:

    def __init__(self, GPIO_pin):
        self.dhtDevice = adafruit_dht.DHT11(GPIO_pin)
        self.error = 0

    def get_temperature(self):
        try:
            if (type(self.dhtDevice.temperature) == type(None)):
                c_temp = f_temp = -1000.0
            else:
                c_temp = float(self.dhtDevice.temperature)
                f_temp = float(c_temp) * 1.8 + 32
        except RuntimeError:
            c_temp = -1000.0
            f_temp = -1000.0
        return [c_temp, f_temp]
    
    def get_humidity(self):
        try:
            humidity = self.dhtDevice.humidity
        except RuntimeError:
            humidity = -1000.0
        return humidity
        
    