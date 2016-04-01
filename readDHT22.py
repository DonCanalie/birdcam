#!/usr/bin/python
import Adafruit_DHT
import datetime

sensor = Adafruit_DHT.DHT22
pin = 4

def getCurrentClimate(ret = False):
    try:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        recorded = datetime.datetime.now()
    except:
        print "An error occured. You have te run the script as root!"
    if ret == True:
        return (str(recorded), "%.1f" % temperature, "%.1f" % humidity)
    else:
        print "'%s', %.2f, %.2f" % (str(recorded), temperature, humidity)    
    
if __name__ == '__main__':
    getCurrentClimate()
