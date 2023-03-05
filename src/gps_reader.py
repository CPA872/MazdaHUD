from gpsdclient import GPSDClient
import time

def read_gps():
    # time.sleep(3)
    print("call read_gps")
    with GPSDClient(host='127.0.0.1') as client:
        for result in client.dict_stream(convert_datetime=True, filter=["TPV"]):
            # print(result)
            # print(type(result))
            # print(result['mode'], result['lat'], result['lon'])
            
            mode = result.get("mode", "n/a")
            if int(mode) == 1 or int(mode) == 2:
                return "-1", "-999", "-999"

            lat  = result.get("lat", "n/a")
            lon = result.get("lon", "n/a")
            alt  = result.get("alt", "n/a")
            
            mode = int(mode)
            if alt == "n/a":
                alt = 100
            if mode == 1 or mode == 2 or lat == "n/a" or lon == "n/a":
                return "-1", "-999", "-999"
            else:
                lat = float(lat)
                lon = float(lon)
                alt = int(alt)
                lat_dir = "N" if lat >= 0 else "S"
                lon_dir = "E" if lon >= 0 else "W"
                lat = abs(lat)
                lon = abs(lon)
                coor = f"{lat:.5f}° {lat_dir}, {lon:.5f}° {lon_dir}"

                return mode, coor, alt