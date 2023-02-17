# utils
import obd_reader
import board
import time
import sys
import multiprocessing

sys.path.insert(1, 'sensor')

import gps_reader
from sensor import sensor_reader

DEMO_MODE = True
DISPLAY_COLORS = ["#33FF00", "#FFC000"]
DEFAUT_FONT = "Consolas"
DISPLAY_MODES = ["normal_imperial", "normal_metric", "zen_imperial", "zen_metric", "full_imperial", "full_metric"]
curr_color = 0
curr_mode  = 0

try:
    obd = obd_reader.OBDReader(True, DEMO_MODE)
    obd.start_async_watch()
except:
    obd.connection.close()
    print("OBD initialization error")
    

dht_pin = board.D14
sensor_reader = sensor_reader.SensorReader(dht_pin)
gps_reader = gps_reader.GPSReader()

def update_sensors():
    while True:
        sensor_reader.sensor_all_update()
        time.sleep(0.01)
