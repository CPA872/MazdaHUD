import sensor.sensor as sensor
import board
import time

dht_pin = board.D14
sensors = sensor.Sensor(dht_pin)

while True:
    print("=============================")
    sensors.sensor_all_update()
    #print(sensors.acceleration, sensors.heading_angle, sensors.compass_direction)
    print("Acceleration: %.2fm/s^2" %sensors.acceleration)
    print("Direction: %.0f" %sensors.heading_angle+u'\u00b0'+sensors.compass_direction)
    
    if (sensors.c_temp != -1000.0 and sensors.f_temp != -1000.0 and sensors.humidity != -1000.0):
        print ("Temperature: %.1f" %sensors.c_temp+u'\u00b0'+"C / %.1f" %sensors.f_temp+u'\u00b0'+"F")
        print("Humidity: %.1f" %sensors.humidity+"%")
    
    print("Brightness level:", sensors.visible_brightness)
    time.sleep(2)
    