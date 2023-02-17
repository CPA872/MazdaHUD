from gpsdclient import GPSDClient
from PyQt5.QtCore import QThread, QRunnable

import time

class GPSReader(QThread):
    
    def __init__(self) -> None:
        super().__init__()
        self.mode = 1
        self.coor = "--.-----° N, --.------° E"
        self.alt  = 0
        

    def run(self):
        # time.sleep(3)
        print("call read_gps")
        with GPSDClient(host='127.0.0.1') as client:
            # while not self.isInterruptionRequested():
                            
            for result in client.dict_stream(convert_datetime=True, filter=["TPV"]):
                # print(result)
                # print(type(result))
                # print(result['mode'], result['lat'], result['lon'])
                if self.isInterruptionRequested():
                    return
                
                mode = result.get("mode", "n/a")
                
                lat  = result.get("lat", "n/a")
                lon = result.get("lon", "n/a")
                alt  = result.get("alt", "n/a")
                
                if alt == "n/a":
                    alt = 100
                
                
                lat = float(lat)
                lon = float(lon)
                alt = int(alt)
                lat_dir = "N" if lat >= 0 else "S"
                lon_dir = "E" if lon >= 0 else "W"
                lat = abs(lat)
                lon = abs(lon)
                
                self.alt = alt
                
                if mode == 1 or mode == 2 or lat == "n/a" or lon == "n/a" or alt == "n/a":
                    self.mode = -1
                    self.coor = "--.-----° N, --.------° E"
                    self.alt  = "----"
                
                else:
                    self.coor = f"{lat:.5f}° {lat_dir}, {lon:.5f}° {lon_dir}"
                    self.mode = int(mode)
                
                time.sleep(3)
                print(self.coor, self.mode, self.alt)
    
    def stop(self):
        self.is_stopped = True