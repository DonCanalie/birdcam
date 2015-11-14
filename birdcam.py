""" This script is used to publish a webapp, based on templates/index.html,
 which can be used to watch the webstreams running on a birdcam-surveillance-system.
 Moreover, there is the possibillity to control IR-Light-LED's to light the view. """
import web
import os
import sqlite3
#import RPi.GPIO as GPIO
# https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code/tree/master/Adafruit_DHT_Driver_Python
#import dhtreader
import plotly.plotly as py
import plotly.graph_objs as go

from web import form

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

DHT_TYPE = 22
DHT_SOURCE = GPIO4

DATABASE = "birdcam.db"

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
    form.Textbox("txt1", web.form.notnull, description="Temperature:", style="float: lefty; width: 50px;"),
    form.Textbox("txt2", web.form.notnull, description="Humidity:", style="float: left; width: 50px;"),
    form.Textbox("txt3", web.form.notnull, description="recorded at ", style="float: left; width: 50px;"),
    form.Button("btn", id="btnG3", value="btnRefreshClimate", html="Refresh", class_="off", style="float: left;"),
    form.Button("btn", id="btnY3", value="btnTimeline", html="Timeline", class_="cam", style="float: left;")
)

TOPRIGHT = form.Form(
    form.Button("btn", id="btnR3", value="btnReboot", html="Reboot", class_="off"),
)

def getDBCursor():
    global db
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    return cursor

def getClimateData(limit):
    """ TODO: Evtl. auf dht22 umbauen fuer ganz aktuellen zugriff. Haengt jedoch davon ab, wie schnell der Sensor anwortet. 
        Sonst besser wie gehabt aus der DB lesen """
            
    cursor = getDBCursor()
    commandtext = "SELECT recorded, temperature, humidity FROM climate " \
        "ORDER BY recorded DESC"
        
    if limit:           
        cursor.execute(commandtext + " LIMIT (?)", (limit))
    else:
        cursor.execute(commandtext)
    
    result = cursor.fetchall()
    #print result
    db.close()
    return result

def setClimateData():
    climate_cur = getClimateData("1")
    if len(climate_cur) > 0:
        #print len(climate_cur)
        row = climate_cur[0]
        #print "climate recorded at {0} - temperature: {1}, humidity: {2}".format(
        #    row[0], row[1], row[2])    
        left.txt1.value = row[1]
        left.get('txt2').value = row[2]
        left.txt3.value = row[0]
    return

class Climate(object):
    
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
        
        return plot_url

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
        
        right = RIGHT()
        left = LEFT()
        topright = TOPRIGHT()        
        webcam = WEBCAM1   
        
        setClimateData()
                
        return RENDER.index(right, left, topright, "Raspberry Pi LED Blink", webcam)

    def POST(self):
        """ posting the data from the webpage to Pi """
        global webcam

        # get the data submitted from the web form
        userdata = web.input()
        if userdata.btn == "btnLed0On":
 #           GPIO.output(GPIO0,True) #Turn on the LED
            print "LED0 is ON"   #prints the status in Pi's Terminal
        elif userdata.btn == "btnLed0Off":
  #          GPIO.output(GPIO0,False) #Turn of the LED
            print "LED0 is OFF" #prints the status in Pi's Terminal
        elif userdata.btn == "btnLed1On":
#            GPIO.output(GPIO1,True) #Turn of the LED
            print "LED1 is OFF" #prints the status in Pi's Terminal
        elif userdata.btn == "btnLed1Off":
#            GPIO.output(GPIO1,False) #Turn of the LED
            print "LED1 is OFF" #prints the status in Pi's Terminal
        elif userdata.btn == "btnReboot":
            print "System is going to for reboot!" #prints the status in Pi's Terminal 
            os.system("sudo reboot")   
        elif userdata.btn =="btnRefreshClimate":
            setClimateData() # wird beim refresh eigentlich gemacht. alternativ: nur initial und sonst explizit ausfuehren
        elif userdata.btn == "btnWebcam1":
            print "Switched to Webcam 1" #prints the status in Pi's Terminal
            webcam = WEBCAM1
        elif userdata.btn == "btnWebcam2":
            print "Switched to Webcam 2" #prints the status in Pi's Terminal
            webcam = WEBCAM2     
        elif userdata.btn == "btnTimeline":
            raise web.seeother('/climate')
        
        #raise web.seeother('/') # Geht hier nicht, da der Parameter 'webcam' sich geaendert hat
        return RENDER.index(right, left, topright, "Raspberry Pi LED Blink", webcam)
# run
if __name__ == '__main__':
    web.httpserver.runsimple(APP.wsgifunc(), (SOCKET_IP, SOCKET_PORT))
    #APP.run()

