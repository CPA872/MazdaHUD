import obd

def main():
    print("Using PyOBD, version", obd.__version__)

    # while True:
    connection = obd.OBD() # auto-connects to USB or RF port
    
    print("Established connection with OBDII")
    
    speed_cmd = obd.commands.SPEED # select an OBD command (sensor)
    rpm_cmd   = obd.commands.RPM
    
    # we want
    """ 
        speed
        tach
        gear
        
    """

    response = connection.query(speed_cmd) # send the command, and parse the response

    print(response.value) # returns unit-bearing values thanks to Pint
    print(response.value.to("mph")) # user-friendly unit conversions
    
    while 1:
        pass
    
if __name__ == "__main__":
    main()