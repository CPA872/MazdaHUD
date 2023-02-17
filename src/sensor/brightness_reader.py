import time
import board
import adafruit_tsl2591

#lux - The computed light lux value measured by the sensor.
#visible - The visible light level measured by the sensor.  
#infrared - The infrared light level measured by the sensor. 

class brightnessReader:

    def __init__(self):
        i2c = board.I2C()
        self.sensor = adafruit_tsl2591.TSL2591(i2c)

    def get_lux(self):
        return self.sensor.lux
    
    def get_visible(self):
        return self.sensor.visible
    
    def get_infrared(self):
        return self.sensor.infrared
