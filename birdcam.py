import web
#import RPi.GPIO as GPIO 

from web import form

GPIO0 = 11
GPIO1 = 12
GPIO2 = 13
GPIO3 = 15
GPIO4 = 16
GPIO5 = 18

#GPIO.setmode(GPIO.BOARD) ## setting GPIO pin numbering to Board format --> Use Pin-Number, not GPIO number
#GPIO.setup(GPIO0, GPIO.OUT) ## Setting GPIO 0 on Pin 11 to Output mode
#GPIO.setup(GPIO1, GPIO.OUT) ## Setting GPIO 1 on Pin 12 to Output mode

#Defining the index page
urls = ('/', 'index')

render = web.template.render('templates') #index.html is stored in '/templates' folder

app = web.application(urls, globals())

""" Defining the buttons. 'id' stands for HTML id of the element. 'value' is the value of the button as perceived by Python. 
    'html' is the text displayed in HTML page. 'class_' is HTML class"""
my_form = form.Form(
                    form.Button("btn", id="btnR1", value="btnLed0On", html="LED0 on", class_="on"),
                    form.Button("btn", id="btnG1", value="btnLed0Off", html="LED0 off", class_="off"),
                    form.Button("btn", id="btnR2", value="btnLed1On", html="LED1 on", class_="on"),
                    form.Button("btn", id="btnG2", value="btnLed1Off", html="LED1 off", class_="off"),
                    form.Button("btn", id="btnY1", value="btnWebcam1", html="Webcam 1", class_="cam"), 
                    form.Button("btn", id="btnY2", value="btnWebcam2", html="Webcam 2", class_="cam"), 
)

# define the task of index page
class index:     

    # rendering the HTML page
    def GET(self):     
        global form
        form = my_form()  
        webcam = "1"   
        return render.index(form, "Raspberry Pi LED Blink", webcam)

    # posting the data from the webpage to Pi
    def POST(self):   
        global render     
        global webcam
                
        # get the data submitted from the web form
        userData = web.input()
        if userData.btn == "btnLed0On":
 #           GPIO.output(GPIO0,True) #Turn on the LED
            print "LED0 is ON"   #prints the status in Pi's Terminal
        elif userData.btn == "btnLed0Off":
  #          GPIO.output(GPIO0,False) #Turn of the LED
            print "LED0 is OFF" #prints the status in Pi's Terminal
        elif userData.btn == "btnLed1On":
#            GPIO.output(GPIO1,True) #Turn of the LED
            print "LED1 is OFF" #prints the status in Pi's Terminal        
        elif userData.btn == "btnLed1Off":
#            GPIO.output(GPIO1,False) #Turn of the LED
            print "LED1 is OFF" #prints the status in Pi's Terminal
        elif userData.btn == "btnWebcam1":
            print "Switched to Webcam 1" #prints the status in Pi's Terminal
            webcam ="1"         
        elif userData.btn == "btnWebcam2":
            print "Switched to Webcam 2" #prints the status in Pi's Terminal
            webcam ="2"
                   
        #raise web.seeother('/')    
        return render.index(form, "Raspberry Pi LED Blink", webcam)
# run
if __name__ == '__main__':
    app.run()

