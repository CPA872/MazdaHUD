import time
import smbus
import math

from imusensor.MPU9250 import MPU9250

class IMUReader:
    def __init__(self):
        address = 0x68
        bus = smbus.SMBus(1)
        self.imu = MPU9250.MPU9250(bus, address)
        self.imu.begin()
        self.imu.setAccelRange("AccelRangeSelect2G")

    def get_acceleration(self):
        self.imu.readSensor()
        Ax = self.imu.AccelVals[0]
        Ay = self.imu.AccelVals[1]

        A = math.sqrt(Ax**2 + Ay**2)
        if (Ay < 0):
            A = -A

        return A
    
    def get_heading(self):
        self.imu.readSensor()
        Ax = self.imu.AccelVals[0]
        Ay = self.imu.AccelVals[1]
        Az = self.imu.AccelVals[2]

        Axnorm = Ax/math.sqrt(Ax * Ax + Ay * Ay + Az * Az)
        Aynorm = Ay/math.sqrt(Ax * Ax + Ay * Ay + Az * Az)
        pitch = math.asin(Axnorm)
        roll = -math.asin(Aynorm/math.cos(pitch))

        Magx = self.imu.MagVals[0]
        Magy = self.imu.MagVals[1]
        Magz = self.imu.MagVals[2]

        MagHx = Magx*math.cos(pitch) + Magz*math.sin(pitch)
        MagHy = Magx*math.sin(roll)*math.sin(pitch) + Magy*math.cos(roll) - Magz*math.sin(roll)*math.cos(pitch)
        Heading = 180 * math.atan2(MagHy, MagHx) / math.pi
        if (Heading < 0):
            Heading = Heading + 360
        
        #To improve
        return Heading
