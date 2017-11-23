
#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import smtplib
GPIO.setwarnings(False)
#GPIO SETUP
channel = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)
GPIO.setup(16,GPIO.OUT)
GPIO.setwarnings(False)
GPIO.setup(4, GPIO.IN) 
GPIO.setup(18,GPIO.OUT)
fromaddr = 'Correo del remitente'
toaddrs  = 'Correo de destinatario'
msg = 'Movimiento detectado'
                 
# Datos
username = 'Correo a usar como host'
password = 'Contraseña de dicho correo'
 
def callback(channel):
        if GPIO.input(channel):
            if (GPIO.input(18)):    
                # Enviando el correo
                server = smtplib.SMTP('smtp.gmail.com:587')
                server.starttls()
                server.login(username,password)
                server.sendmail(fromaddr, toaddrs, msg)
                server.quit()
                while True:#blink del led
                    inputValue= GPIO.input (4)
                    GPIO.output(16,True)
                    if inputValue == True:
                    	GPIO.output(16,False)
                    	break

 
GPIO.add_event_detect(channel, GPIO.FALLING, bouncetime=300)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(channel, callback)  # assign function to GPIO PIN, Run function on change
try:
# infinite loop
        while True:
                time.sleep(1)

#Correo electronico

except KeyboardInterrupt:

    GPIO.cleanup() #limpia los puertos


    
