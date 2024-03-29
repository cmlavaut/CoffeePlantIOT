import paho.mqtt.client as mqtt
import pandas as pd
import time
from datetime import datetime
import sys
import os
from threading import Thread
import json

broker = "192.168.50.155"
leerCredenciales = open("credenciales.json")
credenciales = json.load(leerCredenciales)
user = credenciales['user']
passwd = credenciales['passwd']
leerCredenciales.close()
topic = sys.argv[1]
path = '../csv/mediciones.csv'
now = datetime.now()
fecha = now.strftime("%d %m %y")
hora = now.strftime("%H:%M:%S")

def guardar(valorA, tabla):
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
    #print(valorA)
    valorA.pop(3)
    valorA.pop(2)
    datos = datos + valorA
    tabla.loc[tabla.shape[0]] = datos
    tabla.to_csv(path, index = False)
    

def on_connect(client, userdata, flags, rc):
    print("conectando al broker", rc)
    client.subscribe(topic)

def on_disconnect(client, userdata,rc):
    if rc != 0:
        print("Unexpected disconnection.")
    print("cerrando el broker",rc)
    client.loop_stop()
    os._exit(0)

def on_message(client, userdata, message):
    global tabla
    print("topic: {} y su mensaje es {}".format(message.topic, message.payload.decode()))
    value = message.payload.decode()
    value = value.split()
    if (len(value) == 7):
        print("valores correctos")
        guardar(value, tabla)
        client.disconnect()

    else:
        print("valores incorrectos")
        


def main():
    global tabla, value
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
    
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.username_pw_set(user,passwd)
    client.connect(broker)
    client.loop_start()
    print("Leyendo: {} {} {}".format(topic,fecha,hora))


def detenerCodigo():
    time.sleep(15)
    print("Cerrando codigo")
    os._exit(0)


if __name__ == "__main__":
    thread = Thread(target=detenerCodigo)
    thread.start()
    main()
