# Germán Andrés Xander 2023

from machine import Pin, Timer, unique_id
import dht
import time
import json
import ubinascii
from collections import OrderedDict
from settings import SERVIDOR_MQTT
from umqtt.robust import MQTTClient

CLIENT_ID = ubinascii.hexlify(unique_id()).decode('utf-8')

mqtt = MQTTClient(CLIENT_ID, SERVIDOR_MQTT,
                  port=8883, keepalive=10, ssl=True)

d = dht.DHT22(Pin(25))
contador = 0
tempMax = False
tempMin = False
flag = False

while True:
    try:
        d.measure()
        temperatura = d.temperature()
        humedad = d.humidity()
        datos = json.dumps(OrderedDict([
            ('temperatura',temperatura),
            ('humedad',humedad)
        ]))
        print(datos)

        if temperatura > 25:
            tempMax = True

        if temperatura < 20:
            tempMin = True

        if tempMax & tempMin & (temperatura > 25):
            flag = True
        
        print("temperatura max", tempMax)
        print("temperatura min", tempMin)

        if flag:
            print("publicando temperatura")
            mqtt.connect()
            mqtt.publish(f"ap/{CLIENT_ID}",datos)
            mqtt.disconnect()     
            flag = False
            tempMax = False
            tempMin = False

    except OSError as e:
        print("sin sensor")
    time.sleep(5)
