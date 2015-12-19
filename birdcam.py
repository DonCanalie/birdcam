#!/usr/bin/python
""" This script is used to publish a webapp, based on templates/index.html,
 which can be used to watch the webstreams running on a birdcam-surveillance-system.
 Moreover, there is the possibillity to control IR-Light-LED's to light the view. """
import web
import os
import json
import sqlite3
import plotly.plotly as py # plotly library
import plotly.graph_objs as go
from climate import Climate
from datetime import datetime
from __builtin__ import True
#import RPi.GPIO as GPIO
# https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code/tree/master/Adafruit_DHT_Driver_Python
#import dhtreader

"""evtl fastcgi statt webpi verwenden, wie hier beschrieben http://davstott.me.uk/index.php/2013/03/17/raspberry-pi-controlling-gpio-from-the-web/"""
from web import form

DEBUG = True
LOG = True

SOCKET_IP = "0.0.0.0"
SOCKET_PORT = 80

GPIO0 = 11
GPIO1 = 12
GPIO2 = 13
GPIO3 = 15
GPIO4 = 16
GPIO5 = 18

WEBCAM1 = "1"
WEBCAM2 = "2"
STREAM1 = "http://raspberrypi2:8080/?action=stream"
STREAM2 = "http://raspberrypi2:8081/?action=stream"

DHT_TYPE = 22
DHT_SOURCE = GPIO4

DATABASE = "birdcam.db"

with open('./plotly_config.json') as config_file:
    plotly_user_config = json.load(config_file)
    py.sign_in(plotly_user_config["plotly_username"], plotly_user_config["plotly_api_key"])

# initialize DHT22-Reader
#dhtreader.init()

# GPIO.BOARD --> Use Pin-Number, not GPIO number
#GPIO.setmode(GPIO.BOARD) ## setting GPIO pin numbering to Board format
#GPIO.setup(GPIO0, GPIO.OUT) ## Setting GPIO 0 on Pin 11 to Output mode
#GPIO.setup(GPIO1, GPIO.OUT) ## Setting GPIO 1 on Pin 12 to Output mode

#Defining the urls
URLS = (
    "/", "Index", 
    "/climate", "Climate"
)

RENDER = web.template.render('templates') #index.html is stored in '/templates' folder
APP = web.application(URLS, globals())

""" Defining the buttons. 'id' stands for HTML id of the element.
    'value' is the value of the button as perceived by Python.
    'html' is the text displayed in HTML page. 'class_' is HTML class"""    
RIGHT = form.Form(
    form.Button("btn", id="btnR1", value="btnLed0On", html="LED0 on", class_="on"),
    form.Button("btn", id="btnG1", value="btnLed0Off", html="LED0 off", class_="off"),
    form.Button("btn", id="btnR2", value="btnLed1On", html="LED1 on", class_="on"),
    form.Button("btn", id="btnG2", value="btnLed1Off", html="LED1 off", class_="off"),
    form.Button("btn", id="btnY1", value="btnWebcam1", html="Webcam 1", class_="cam"),
    form.Button("btn", id="btnY2", value="btnWebcam2", html="Webcam 2", class_="cam"),
)

LEFT = form.Form(
    form.Textbox("txt1", web.form.notnull, description="Temperature:", size="1"),
    form.Textbox("txt2", web.form.notnull, description="Humidity:", size="1"),
    form.Textbox("txt3", web.form.notnull, description="recorded at ", size="1"),
    form.Button("btn", id="btnG3", value="btnRefreshClimate", html="Refresh", class_="off"),
    form.Button("btn", id="btnY3", value="btnTimeline", html="Timeline", class_="cam"),
    form.Textbox("txt4", web.form.notnull, description="Start:", size="1"),
    form.Textbox("txt5", web.form.notnull, description="End:", size="1"),    
)

TOPRIGHT = form.Form(
    form.Button("btn", id="btnR3", value="btnReboot", html="Reboot", class_="off"),
)

class Logger(object):
    def info(self, message):
        self.log(message, 'LOG')
    def debug(self, message):
        self.log(message, 'DEBUG')     
    def log(self, message, type):
        valid = False
        if type == 'LOG' and (LOG | DEBUG):
            valid = True
        if type == 'DEBUG' and DEBUG:
            valid = True
        if valid:
            print  type + ' ' + datetime.now().strftime('%Y-%m-%d  %H:%M:%S') + ': ' + message     

def validate(date_text):
    result = True
    logger = Logger()      
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d  %H:%M:%S')
        logger.debug('validate.date_text - ' + date_text + ' is valid')
    except:
        result = False
        logger.debug('validate.date_text is invalid')        
    return result

def getDBCursor():
    global db
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    return cursor

def getClimateData(columns = "recorded, temperature, humidity", limit = -1, start = -1, end = -1):
    """ TODO: Evtl. auf dht22 umbauen fuer ganz aktuellen zugriff. Haengt jedoch davon ab, wie schnell der Sensor anwortet. 
        Sonst besser wie gehabt aus der DB lesen """
    logger = Logger()       
    cursor = getDBCursor()
    commandtext = "SELECT " + columns + " FROM climate"
    orderby = " ORDER BY recorded DESC"
    where = -1    
    parameters = []
        
    if start >= 0:
        where = " WHERE recorded >= (?)" 
        parameters.append(start) 
    if end >= 0:
        if where != -1:
            where += " AND recorded <= (?)"            
        else:
            where = " WHERE recorded <= (?)"            
        parameters.append(end) 
    if where != -1:
        commandtext += where
    if limit >= 0:           
        orderby += " LIMIT (?)"#, (limit))
        parameters.append(limit)
    commandtext += orderby
    logger.debug('getClimateData.commandtext - ' + commandtext)
    logger.debug('getClimateData.parameters - ' + ''.join(str(p) for p in parameters))
    if (len(parameters) > 0):
        cursor.execute(commandtext, parameters)
    else:
        cursor.execute(commandtext)
    
    result = cursor.fetchall()
    #print result
    db.close()
    logger.debug('getClimateData.result - ' + ''.join(str(r) for r in result))
    return result

def setClimateData():
    climate_cur = getClimateData("recorded, temperature, humidity", "1")
    if len(climate_cur) > 0:
        row = climate_cur[0]
        left.txt1.value = row[1]
        left.get('txt2').value = row[2]
        left.txt3.value = row[0]
    return

"""class Climate(object):
    
    def GET(self):
        # Simply use this https://github.com/Pyplate/rpi_temp_logger
        # https://plot.ly/python/time-series/
        

        data = [
            go.Scatter(
                x=['2013-10-04 22:23:00', '2013-11-04 22:23:00', '2013-12-04 22:23:00'],
                y=[1, 3, 6]
            )
        ]
        
        plot_url = py.plot(data, filename='date-axes')
        
        return plot_frame"""

class Index(object):
    """ define the task of index page """
    
#    def __init__(self):
#        self.webcam ) 

    def GET(self):
        """ rendering the HTML page """
        global webcam
        global topright
        global left
        global right
        global center
        
        logger = Logger()
        
        right = RIGHT()
        left = LEFT()
        topright = TOPRIGHT()        
        webcam = WEBCAM1  
        center = STREAM1 
        
        setClimateData()
                
        return RENDER.index(right, left, topright, "Raspberry Pi LED Blink", webcam, center)

    def POST(self):
        """ posting the data from the webpage to Pi """
        global webcam
        global center
        
        logger = Logger()

        # get the data submitted from the web form
        userdata = web.input()
        if userdata.btn == "btnLed0On":
 #           GPIO.output(GPIO0,True) #Turn on the LED
            logger.info('Index.POST - LED0 is ON')   #prints the status in Pi's Terminal
        elif userdata.btn == "btnLed0Off":
  #          GPIO.output(GPIO0,False) #Turn of the LED
            logger.info('Index.POST - LED0 is OFF') #prints the status in Pi's Terminal
        elif userdata.btn == "btnLed1On":
#            GPIO.output(GPIO1,True) #Turn of the LED
            logger.info('Index.POST - LED1 is ON') #prints the status in Pi's Terminal
        elif userdata.btn == "btnLed1Off":
#            GPIO.output(GPIO1,False) #Turn of the LED
            logger.info('Index.POST - LED1 is OFF') #prints the status in Pi's Terminal
        elif userdata.btn == "btnReboot":
            logger.info('Index.POST - System is going to for reboot!') #prints the status in Pi's Terminal 
            os.system("sudo reboot")   
        elif userdata.btn =="btnRefreshClimate":
            setClimateData() # wird beim refresh eigentlich gemacht. alternativ: nur initial und sonst explizit ausfuehren
        elif userdata.btn == "btnWebcam1":
            logger.info('Index.POST - Switched to Webcam 1') #prints the status in Pi's Terminal
            webcam = WEBCAM1
            center = STREAM1
        elif userdata.btn == "btnWebcam2":
            logger.info('Index.POST - Switched to Webcam 2') #prints the status in Pi's Terminal
            webcam = WEBCAM2     
            center = STREAM2
        elif userdata.btn == "btnTimeline":
            start = -1
            end = -1
            limit = -1
            left.validates()
            if validate(left.txt4.value) == True:
                start = left.txt4.value                
                logger.debug('Index.POST.btnTimeLine.start - ' + start)
            if validate(left.txt5.value == True):
                end = left.txt5.value
                logger.debug('Index.POST.btnTimeLine.end - ' + end)                
            x = getClimateData("recorded", limit, start, end)
            y = getClimateData("temperature", limit, start, end)
            logger.debug('Index.POST.btnTimeLine.x - ' + ''.join(str(r) for r in x))
            logger.debug('Index.POST.btnTimeLine.y - ' + ''.join(str(r) for r in y))
            center = Climate().plot(x, y)
            #raise web.seeother('/climate')
        
        print center
        #raise web.seeother('/') # Geht hier nicht, da der Parameter 'webcam' sich geaendert hat
        return RENDER.index(right, left, topright, "Raspberry Pi LED Blink", webcam, center)
# run
if __name__ == '__main__':
    web.httpserver.runsimple(APP.wsgifunc(), (SOCKET_IP, SOCKET_PORT))
    #APP.run()

