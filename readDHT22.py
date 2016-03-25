#!/usr/bin/python
import Adafruit_DHT
import datetime

sensor = Adafruit_DHT.DHT22
pin = 4

humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

print "'%s', %.2f, %.2f" % (str(datetime.datetime.now()), temperature, humidity)
