import webiopi
import datetime
 
GPIO = webiopi.GPIO
 
ON = 18 # GPIO pin using BCM numbering
CLOSE = 20
ACT = 21
MOVE = 16
 
# setup function is automatically called at WebIOPi startup
def setup():
    GPIO.setFunction(ON, GPIO.OUT)
    GPIO.setFunction(ACT, GPIO.OUT)
 
# loop function is repeatedly called by WebIOPi
def loop():
    GPIO.digitalRead(ON)
    GPIO.digitalRead(CLOSE)
    GPIO.digitalRead(MOVE)
    webiopi.sleep(1)

def destroy():
    GPIO.digitalWrite(ON, GPIO.LOW)
