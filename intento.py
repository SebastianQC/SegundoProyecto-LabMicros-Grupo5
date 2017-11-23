import os
import cv2
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

camera_port = 0

ramp_frames = 30

camera = cv2.VideoCapture(camera_port)

def get_image():

    retval,im = camera.read()
    return im
for i in xrange(ramp_frames):
    temp = get_image()

camera_capture = get_image()
file = "imagen.png"
cv2.imwrite(file, camera_capture)
del(camera)

time.sleep(12)

fromaddr = "Correo remitente/host"
toaddr = "Correo destinatario"

img_data = open("imagen.png",'rb').read()
msg = MIMEMultipart()

msg ['From'] = fromaddr
msg ['To'] = toaddr
msg ['Subject'] = "Intento7"


text = MIMEText("A dormir un toque")
msg.attach(text)

image = MIMEImage(img_data, name = os.path.basename("/home/pi/home/pi/Archivos Proyecto Micro Grupo 5 II Semetre 2017 (JJJS)/imagen.png"))
msg.attach(image)

server = smtplib. SMTP ('smtp.gmail.com',587)
server.ehlo()
server.starttls()
server.ehlo()
server.login (fromaddr,"Contraseña del correo remitente/host")
text1 = msg.as_string()
server.sendmail(fromaddr,toaddr,text1)
server.quit()
