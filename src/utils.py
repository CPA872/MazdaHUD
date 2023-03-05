# utils
import obd_reader

# global positioning parameters (upper left corner coordinates)
# 800x480
RPM_BAR_VALUE = (50, 50)
RPM_BAR_LABEL = (30, 750)
RPM_BAR = (50, 100)

GPS_LABEL = (200, 50)
GPS_SPEED_ALT = (300, 50)

IAT_LABEL = (650, 750)

SMALL_FONT_SIZE = 30

LIGHT_GREEN = "#11ff00"
DEFAUT_FONT = "Consolas"

try:
    obd = obd_reader.OBDReader(True)
    obd.start_async_watch()
except:
    obd.connection.close()
    print("OBD initialization error")