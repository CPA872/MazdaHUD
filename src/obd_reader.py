import obd
import time

from datetime import datetime


class OBDReader:

    def __init__(self):
        self.connection = obd.Async("/dev/ttyACM1")  # auto-connects to USB or RF port

    async def start_async_watch(self):
        self.connection.watch(obd.commands.SPEED)
        self.connection.watch(obd.commands.RPM)
        self.connection.watch(obd.commands.COOLANT_TEMP)

        self.connection.start()

    def get_speed(self):
        response = self.connection.query(obd.commands.SPEED)
        return int(response.value.magnitutde), int(response.value.to('mph').magnitude)

    def get_rpm(self):
        response = self.connection.query(obd.commands.RPM)
        return int(response.value.magnitude)

    def new_coolant_temp(self):
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


