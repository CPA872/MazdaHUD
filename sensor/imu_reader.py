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
        Heading = self.sensorfusion.yaw
        if (Heading < 0):
            Heading = Heading + 360
        elif (Heading > 360):
            Heading = Heading - 360
        
        #To improve
        return Heading
