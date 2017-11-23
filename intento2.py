import os
import cv2
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

#Simulacion de la parte de sensores y pagina web. Estos parametros se ingresaran de manera distinta al final.
#El correo de destino por medio de la pagina y lo de empezar lo indicara la pagina y los sensores
a = 1
toaddr = raw_input("Ingrese destinatario: ")
valor = raw_input("Digite 'a' para empezar: ")

#Variables importantes para la parte de la camara
camera_port = 0 #puerto que utiliza la camara en la computadora
ramp_frames = 30 #para tomar un foto de buena calidad. Espera a que la camara se estabilice

while(a):

    #seccion de codigo que se ejecuta cuando hay deteccion de movimiento y la vigilancia esta activa
    if valor == "a":
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

        time.sleep(8)#tiempo que hay entre ambos codigos. Para darle tiempo a la imagen de crearse bien y poder ser enviada

        hora = time.strftime("%c")#se obtiene la hora del sistema
        hh1 = "Fecha y hora: " + hora #se le agrega el mensaje de fecha y hora
        

        fromaddr = "correo del remitente/host" #correo que sirve de host
       

        img_data = open("imagen.png",'rb').read() #leer el archivo que se envia
        msg = MIMEMultipart() #para crear un correo con sus distintas partes
        #Remitente, destinatario, asunto, cuerpo y archivo adjunto

        msg ['From'] = fromaddr
        msg ['To'] = toaddr
        msg ['Subject'] = "Video Vigilancia"


        text = MIMEText("Foto tomada por la camara." + " " + hh1)
        msg.attach(text)
        
        #se adjunta el la imagen al correo. Agregar la carpeta en la cual se ubica
        image = MIMEImage(img_data, name = os.path.basename("/home/pi/home/pi/Archivos Proyecto Micro Grupo 5 II Semetre 2017 (JJJS)/imagen.png"))
        msg.attach(image)
        #objeto smtp, se crea el host para poder enviar el correo
        server = smtplib. SMTP ('smtp.gmail.com',587)
        #server.ehlo()
        server.starttls()
        #server.ehlo()
        server.login (fromaddr,"Contraseña del correo remitente/host")#se entra al host
        text1 = msg.as_string() #el mensaje a enviar convierte a string para poder usarlo
        server.sendmail(fromaddr,toaddr,text1)#se crea el correo a enviar
        server.quit()#se sale del hosy

        #Parte de simulacion de comportamiento.
        pregunta = raw_input("Seguir (a = Si // b = No): ")

        if pregunta == "a":
            a = 1
        else:
            a= 0

    else:
        break

