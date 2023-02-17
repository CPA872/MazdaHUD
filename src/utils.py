# utils
import obd_reader
import board
import time
import sys
import multiprocessing

sys.path.insert(1, 'sensor')

from sensor import sensor_reader

DEMO_MODE = True
LIGHT_GREEN = "#11ff00"
DEFAUT_FONT = "Consolas"

try:
    obd = obd_reader.OBDReader(True, True)
    obd.start_async_watch()
except:
    obd.connection.close()
    print("OBD initialization error")
    

dht_pin = board.D14
sensors = sensor_reader.SensorReader(dht_pin)

def update_sensors():
    while True:
        sensors.sensor_all_update()
        time.sleep(0.01)