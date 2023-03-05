import sensor_main
import board
import time

dht_pin = board.D14
sensors = sensor_main.sensor(dht_pin)

while True:
    print("=============================")
    sensors.sensor_all_update()
    print(sensors.acceleration, sensors.heading)

    if (sensors.c_temp != -1000.0 and sensors.f_temp != -1000.0 and sensors.humidity != -1000.0):
        print(sensors.c_temp, sensors.f_temp, sensors.humidity)
    
    print(sensors.visible_brightness)
    time.sleep(2)