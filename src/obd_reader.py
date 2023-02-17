import obd
import time

from datetime import datetime

class OBDReader:

    def __init__(self, is_async, is_demo):
        self.is_demo = is_demo
        if not is_demo:
            if is_async:
                self.connection = obd.Async("/dev/ttyUSB0")  
            else:
                self.connection = obd.OBD("/dev/ttyUSB0")

    def start_async_watch(self):
        if self.is_demo:
            return
        
        self.connection.watch(obd.commands.SPEED)
        self.connection.watch(obd.commands.RPM)
        self.connection.watch(obd.commands.COOLANT_TEMP)

        self.connection.start()

    def get_speed(self):
        if self.is_demo:
            return 101, 163
        
        # print("call get speed")
        response = self.connection.query(obd.commands.SPEED)
        # print(response.value.to('mph'))
        # print(int(response.value.magnitude), int(response.value.to('mph').magnitude))
        return int(response.value.to('mph').magnitude), int(response.value.magnitude) 

    def get_rpm(self):
        if self.is_demo:
            return 4350
        response = self.connection.query(obd.commands.RPM)
        # print(response, type(response))
        # print(response.value, type(response.value))
        # print(response.value.magnitude, type(response.value.magnitude))

        return int(response.value.magnitude)

    def get_coolant_temp(self):
        if self.is_demo:
            return 95
        response = self.connection.query(obd.commands.COOLANT_TEMP)
        return int(response.value.magnitude)

    def read_obd_blocking(self):
        speed_cmd = obd.commands.SPEED  # select an OBD command (sensor)
        rpm_cmd = obd.commands.RPM
        coolant_cmd = obd.commands.COOLANT_TEMP

        while True:
            response_speed = self.connection.query(speed_cmd)  # kph
            response_rpm = self.connection.query(rpm_cmd)
            response_cool = self.connection.query(coolant_cmd)

            now = datetime.now().strftime("%H:%M:%S")
            print(f"[{now}] SPD: {response_speed.value}, RPM: {response_rpm}, Coolant: {response_cool.value}")
            time.sleep(0.5)


if __name__ == "__main__":
    reader = OBDReader(False)
    reader.read_obd_blocking()
