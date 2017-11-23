import os
import cv2
import smtplib
import time
import RPi.GPIO as GPIO
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

#Simulacion de la parte de sensores y pagina web. Estos parametros se ingresaran de manera distinta al final.
#El correo de destino por medio de la pagina y lo de empezar lo indicara la pagina y los sensores
GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(20,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
b=1

while(b):
    
    if(GPIO.input(18)):
        a=1 #condicion para activar el sistema
        b=0

#Variables importantes para la parte de la camara
camera_port = 0 #puerto que utiliza la camara en la computadora
ramp_frames = 30 #para tomar un foto de buena calidad. Espera a que la camara se estabilice

try:
    while(a):

        if(GPIO.input(18)):  #condicion de la pagina web      

            def RCtime(PiPin):
                carga = 0
                #Para descargar el capa
                GPIO.setup(PiPin,GPIO.OUT)
                GPIO.output(PiPin, GPIO.LOW)
                time.sleep(0.1)
                #Volver a poner el pin como entrada
                GPIO.setup(PiPin, GPIO.IN)

                while(GPIO.input(PiPin) == GPIO.LOW):
                    carga +=1
                return carga

            #seccion de codigo que se ejecuta cuando hay deteccion de movimiento y la vigilancia esta activa
            if RCtime(22) > 120:
                GPIO.output(20,True)
                print "Enviando"
                #seccion para tomar la foto
                camera = cv2.VideoCapture(camera_port)

                def get_image():

                    retval,im = camera.read()
                    return im
                #para estabilizar la luz de la camara
                for i in xrange(ramp_frames):
                    temp = get_image()

                camera_capture = get_image() #imagen que se utiliza
                file = "imagen.png" #nombre de la imagen que se guarda
                cv2.imwrite(file, camera_capture)#se crea la imagen
                del(camera)#se cierra el uso de la camara

                time.sleep(2)#tiempo que hay entre ambos codigos. Para darle tiempo a la imagen de crearse bien y poder ser enviada

                GPIO.output(20,False)

                hora = time.strftime("%c")#se obtiene la hora del sistema
                hh1 = "Fecha y hora: " + hora #se le agrega el mensaje de fecha y hora

                toaddr = 'Correo de destinatario'
                fromaddr = 'Correo del remitente' #correo que sirve de host


                img_data = open("imagen.png",'rb').read() #leer el archivo que se envia
                msg = MIMEMultipart() #para crear un correo con sus distintas partes
                #Remitente, destinatario, asunto, cuerpo y archivo adjunto

                msg ['From'] = fromaddr
                msg ['To'] = toaddr
                msg ['Subject'] = "Video Vigilancia"


                text = MIMEText("Foto tomada por la camara ." + " " + hh1)

                msg.attach(text)


                #se adjunta el la imagen al correo. Agregar la carpeta en la cual se ubica
                image = MIMEImage(img_data, name = os.path.basename("/home/pi/ProyectoG5/imagen.png"))
                msg.attach(image)
                #objeto smtp, se crea el host para poder enviar el correo
                server = smtplib. SMTP ('smtp.gmail.com',587)
                #server.ehlo()
                server.starttls()
                #server.ehlo()
                server.login (fromaddr,"contraseña del correo host")#se entra al host
                text1 = msg.as_string() #el mensaje a enviar convierte a string para poder usarlo
                server.sendmail(fromaddr,toaddr,text1)#se crea el correo a enviar
                server.quit()#se sale del hosy
                print "Enviado"
                #Parte de simulacion de comportamiento.

            else:
                print "Nada detectado"
                

        else: #por si el pin 18 se pone en bajo, se apaga el sistema
            a=0
            GPIO.output(18, GPIO.LOW)
            #GPIO.cleanup() #limpia los puertos
    

except KeyboardInterrupt:

    GPIO.cleanup() #limpia los puertos
