from gpsdclient import GPSDClient

def read_gps():
    with GPSDClient(host='127.0.0.1') as client:
        for result in client.dict_stream(convert_datetime=True, filter=["TPV"]):
            
            mode = result.get("mode", "n/a")
            lat  = result.get("lat", "n/a")
            long = result.get("lon", "n/a")
            alt  = result.get("alt", "n/a")
            
            mode = int(mode)
            if mode == 1 or mode == 2:
                return (-1, -999, -999, -999)
            else:
                lat = "%.5f" % float(lat)
                long = "%.5f" % float(long)
                alt = "%d" % int(alt)
                return (mode, lat, long, alt)
            

print(read_gps())
