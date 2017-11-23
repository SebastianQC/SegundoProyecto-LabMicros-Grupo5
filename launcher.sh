#1/bin/sh
# launcher.sh
# navigate to home directory,then to this directory, then execute python script$

cd /
cd home/pi/ProyectoG5/
sudo python sw401.py & sudo python intento.py #Se ejecutan los archivos python en paralelo: sw401: archivo de sensor de vibraciones; intento: archivo proyecto
cd /
