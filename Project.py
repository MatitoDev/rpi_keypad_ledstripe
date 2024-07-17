import time
from rpi_ws281x import *
import RPi.GPIO as GPIO
import Keypad
ROWS = 4        # number of rows of the Keypad
COLS = 4        #number of columns of the Keypad
keys =  [   '1','2','3','A',    #key code
            '4','5','6','B',
            '7','8','9','C',
            '*','0','#','D'     ]
rowsPins = [36,38,40,37]        #connect to the row pinouts of the keypad
colsPins = [35,33,31,29]         #connect to the column pinouts of the keypad

# LED strip configuration:
LED_COUNT      = 8      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 80     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

class Led:
    def __init__(self):
        #Control the sending order of color data
        self.ORDER = "RGB"  
        # Create NeoPixel object with appropriate configuration.
        self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        # Intialize the library (must be called once before other functions).
        self.strip.begin()

led=Led()

def set_all(col):
    for i in range (8):
        led.strip.setPixelColor(i,col)
        led.strip.show()

def set_delayed(col,sleep):
    for i in range (8):
        led.strip.setPixelColor(i,col)
        led.strip.show()
        time.sleep(sleep)
        
if __name__ == '__main__':
    print ('Program is starting ... ')
    col_red=Color(255,0,0)
    col_green=Color(13,140,13)
    col_yellow=Color(255,165,34)
    col_off=Color(0,0,0)

    code=['7','3','3','9']
    pressed=[]
    try:
        while True:
            keypad = Keypad.Keypad(keys,rowsPins,colsPins,ROWS,COLS)    #create Keypad object
            key = keypad.getKey()#obtain the state of keys
            if(key != keypad.NULL):  #if there is key pressed, print its key code.
                pressed.append(key)
            
            if len(pressed) == 0:
                set_all(col_red)
            else:
                set_all(col_yellow)
                    
            if len(pressed) == 4:
                for t in range (2):
                    set_delayed(col_off,0.1)
                    set_delayed(col_yellow,0.1)

                if pressed == code:
                    set_all(col_green)
                    time.sleep(3)
                else:
                    for t in range (3):
                        set_all(col_red)
                        time.sleep(0.5)
                        set_all(col_off)
                        time.sleep(0.5)
                pressed.clear()
                
                      
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        for i in range(8):
            led.strip.setPixelColor(i, Color(0,0,0))
        led.strip.show()
        GPIO.cleanup()