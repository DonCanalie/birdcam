import web
import RPi.GPIO as GPIO 

from web import form

GPIO0 = 11
GPIO1 = 12
GPIO2 = 13
GPIO3 = 15
GPIO4 = 16
GPIO5 = 18

GPIO.setmode(GPIO.BOARD) ## setting GPIO pin numbering to Board format
GPIO.setup(GPIO0, GPIO.OUT) ## Setting GPIO 0 on Pin 11 to Output mode
#Defining the index page
urls = ('/', 'index')
render = web.template.render('templates') #index.html is stored in '/templates' folder
app = web.application(urls, globals())

""" Defining the buttons. 'id' stands for HTML id of the element. 'value' is the value of the button as perceived by Python. 
    'html' is the text displayed in HTML page. 'class_' is HTML class"""
my_form = form.Form(
 form.Button("btn", id="btnR", value="btnLed0On", html="LED0 on", class_="on"),
 form.Button("btn", id="btnG", value="btnLed0Off", html="LED0 off", class_="off"),
 
)

# define the task of index page
class index:
    # rendering the HTML page
    def GET(self):
        form = my_form()
        return render.index(form, "Raspberry Pi LED Blink")

    # posting the data from the webpage to Pi
    def POST(self):
        # get the data submitted from the web form
        userData = web.input()
        if userData.btn == "btnLed0On":
            GPIO.output(GPIO0,True) #Turn on the LED
            print "LED is ON"   #prints the status in Pi's Terminal
        elif userData.btn == "btnLed0Off":
            GPIO.output(GPIO0,False) #Turn of the LED
            print "LED is OFF" #prints the status in Pi's Terminal
        raise web.seeother('/')
# run
if __name__ == '__main__':
    app.run()

