""" This script is used to publish a webapp, based on templates/index.html,
 which can be used to watch the webstreams running on a birdcam-surveillance-system.
 Moreover, there is the possibillity to control IR-Light-LED's to light the view. """
import web
#import RPi.GPIO as GPIO

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

# GPIO.BOARD --> Use Pin-Number, not GPIO number
#GPIO.setmode(GPIO.BOARD) ## setting GPIO pin numbering to Board format
#GPIO.setup(GPIO0, GPIO.OUT) ## Setting GPIO 0 on Pin 11 to Output mode
#GPIO.setup(GPIO1, GPIO.OUT) ## Setting GPIO 1 on Pin 12 to Output mode

#Defining the index page
URLS = ('/', 'Index')
RENDER = web.template.render('templates') #index.html is stored in '/templates' folder
APP = web.application(URLS, globals())

""" Defining the buttons. 'id' stands for HTML id of the element.
    'value' is the value of the button as perceived by Python.
    'html' is the text displayed in HTML page. 'class_' is HTML class"""
CONTROLLER = form.Form(
    form.Button("btn", id="btnR1", value="btnLed0On", html="LED0 on", class_="on"),
    form.Button("btn", id="btnG1", value="btnLed0Off", html="LED0 off", class_="off"),
    form.Button("btn", id="btnR2", value="btnLed1On", html="LED1 on", class_="on"),
    form.Button("btn", id="btnG2", value="btnLed1Off", html="LED1 off", class_="off"),
    form.Button("btn", id="btnY1", value="btnWebcam1", html="Webcam 1", class_="cam"),
    form.Button("btn", id="btnY2", value="btnWebcam2", html="Webcam 2", class_="cam"),
)

class Index(object):
    """ define the task of index page """
    
#    def __init__(self):
#        self.webcam ) 

    def GET(self):
        """ rendering the HTML page """
        global webcam
        global form
        form = CONTROLLER()
        webcam = WEBCAM1
        return RENDER.index(form, "Raspberry Pi LED Blink", webcam)

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
        elif userdata.btn == "btnWebcam1":
            print "Switched to Webcam 1" #prints the status in Pi's Terminal
            webcam = WEBCAM1
        elif userdata.btn == "btnWebcam2":
            print "Switched to Webcam 2" #prints the status in Pi's Terminal
            webcam = WEBCAM2

        #raise web.seeother('/')
        return RENDER.index(form, "Raspberry Pi LED Blink", webcam)
# run
if __name__ == '__main__':
    web.httpserver.runsimple(APP.wsgifunc(), (SOCKET_IP, SOCKET_PORT))
    #APP.run()

