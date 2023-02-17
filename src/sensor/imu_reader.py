import time
import smbus
import math

from imusensor.MPU9250 import MPU9250
from imusensor.filters import kalman 

class IMUReader:
    def __init__(self):
        address = 0x68
        bus = smbus.SMBus(1)
        self.imu = MPU9250.MPU9250(bus, address)
        self.imu.begin()
        self.imu.setAccelRange("AccelRangeSelect2G")
#        self.imu.caliberateAccelerometer()
#        self.imu.caliberateMagPrecise()
        self.mag_declination = 11
        self.sensorfusion = kalman.Kalman()
        self.imu.readSensor()
        self.imu.computeOrientation()
        self.sensorfusion.roll = self.imu.roll
        self.sensorfusion.pitch = self.imu.pitch
        self.sensorfusion.yaw = self.imu.yaw
        self.currTime = time.time()

    def get_acceleration(self):
        self.imu.readSensor()
        Ax = self.imu.AccelVals[0]
        Ay = self.imu.AccelVals[1]

        A = math.sqrt(Ax**2 + Ay**2)
        if (Ax < 0):
            A = -A

        return A
    
    def get_heading(self):
        self.imu.readSensor()
        self.imu.computeOrientation()

        newTime = time.time()
        dt = newTime - self.currTime
        self.currTime = newTime

        self.sensorfusion.computeAndUpdateRollPitchYaw(self.imu.AccelVals[0], self.imu.AccelVals[1], self.imu.AccelVals[2], self.imu.GyroVals[0], self.imu.GyroVals[1], self.imu.GyroVals[2],\
											self.imu.MagVals[0], self.imu.MagVals[1], self.imu.MagVals[2], dt)
        heading_angle = self.sensorfusion.yaw + self.mag_declination
        if (heading_angle < 0):
            heading_angle = heading_angle + 360
        elif (heading_angle > 360):
            heading_angle = heading_angle - 360

        compass_direction = 0
        heading_angle = 360 - heading_angle
        if (heading_angle >= 0 and heading_angle < 22.5) or (heading_angle >= 337.5 and heading_angle <= 360):
            compass_direction = "N"
        elif (heading_angle >= 22.5 and heading_angle < 67.5):
            compass_direction = "NE"
        elif (heading_angle >= 67.5 and heading_angle < 112.5):
            compass_direction = "E"        
        elif (heading_angle >= 112.5 and heading_angle < 157.5):
            compass_direction = "SE"
        elif (heading_angle >= 157.5 and heading_angle < 202.5):
            compass_direction = "S"
        elif (heading_angle >= 202.5 and heading_angle < 247.5):
            compass_direction = "SW"
        elif (heading_angle >= 247.5 and heading_angle < 292.5):
            compass_direction = "W"
        elif (heading_angle >= 292.5 and heading_angle < 337.5):
            compass_direction = "NW"
        return [heading_angle, compass_direction]

    
