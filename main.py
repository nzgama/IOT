# Germán Andrés Xander 2023

from machine import Pin
import dht
import time
import json
from collections import OrderedDict

d = dht.DHT22(Pin(25))
print("Sensor temperatura & humedad ...")
contador=0

while True:
    try:
        d.measure()
        temperatura=d.temperature()
        humedad=d.humidity()
        datos=json.dumps(OrderedDict([
            ('temperatura',temperatura),
            ('humedad',humedad)
        ]))
        print(datos)
    except OSError as e:
        print("sin sensor")

    time.sleep(20)