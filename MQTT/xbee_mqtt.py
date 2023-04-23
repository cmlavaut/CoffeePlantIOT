import serial
import time
import sys
import os
import pandas as pd
from datetime import datetime
import paho.mqtt.client as mqtt
import json
from threading import Thread

path = '/home/kmi/CoffeePlantIOT/csv/mediciones.csv'
broker = '192.168.50.155'
leercredenciales = open('credenciales.json',mode = 'r')
credenciales = json.load(leercredenciales)
user = credenciales['user']
paswd = credenciales['passwd']
leercredenciales.close()

def guardar(valorA,tabla):
        now = datetime.now()
        now_fecha = now.strftime("%d %m %y")
        now_hora = now.strftime("%H:%M:%S")
        try:
            tabla.insert(0, "Fecha", now_fecha)
            tabla.insert(1, "Hora", now_hora)
        except:
            #print("ya existe columnas de hora y fecha")
            pass            
        datos = [now_fecha, now_hora]
        datos = datos + valorA
        tabla.loc[tabla.shape[0]] = datos
        tabla.to_csv(path, index = False)
        print(tabla)


def main():
    #Leeer datos anteriores
    try:
        tabla = pd.read_csv(path)
    except:
        dicc = {
            "Place" : [],
            "humedad_suelo" : [],
            "humedad_amb" : [],
            "temperatura" :[],
            "status_agua" : [],
        }
        tabla = pd.DataFrame.from_dict(dicc)
        tabla.to_csv(path,index= False)
    #Comunciacion Serial
    arduino = serial.Serial()
    try:
        puerto= sys.argv[1]
        arduino.port= puerto
        arduino.baudrate = 115200
        topic = sys.argv[2]
        arduino.open()
    except:
        print("nothing conected")
        quit()
    
    arduino.flushInput()
    client = mqtt.Client()
    client.username_pw_set(user,paswd)
    client.connect(broker, 1883)
    sensor = arduino.readline()
    client.publish(topic, sensor)
    sensor = sensor.decode()
    value= sensor.split()
    #print(value)
    if (len(value)==5):
        print("valores correctos")
        guardar(value,tabla)
        client.loop_stop()
        client.disconnect()
        os._exit(0)
    else:
        print("valores incorrectos")
        main()

    arduino.close()

def detener():
    time.sleep(10)
    print("cerrando codigo")
    os._exit(0)


if __name__ == "__main__":
    thread = Thread(target=detener)
    thread.start()
    main()
