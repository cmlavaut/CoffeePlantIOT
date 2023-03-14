import paho.mqtt.client as mqtt
import pandas as pd
import time
from datetime import datetime
import sys

broker = "192.168.0.2"
topic = sys.argv[1]
path = '../csv/datos_new.csv'

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
    datos = datos + valorA
    tabla.loc[tabla.shape[0]] = datos
    tabla.to_csv(path, index = False)
    

def on_connect(client, userdata, flags, rc):
    print("conectando al broker", rc)
    client.subscribe(topic)

def on_message(client, userdata, message):
    global tabla
    print("topic: {} y su mensaje es {}".format(message.topic, message.payload.decode()))
    value = message.payload.decode()
    value = value.split()
    if (len(value) == 4):
        print("valores correctos")
        guardar(value, tabla)
        client.disconnect()
    else:
        print("valores incorrectos")
        


def main():
    global tabla
    try:
        tabla = pd.read_csv(path)
    except:
        dicc = {
            "Place" : [],
            "humedad_suelo" : [],
            "humedad_amb" : [],
            "temperatura" :[],
        }
        tabla = pd.DataFrame.from_dict(dicc)
        tabla.to_csv(path,index= False)
    
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker)
    client.loop_forever()

if __name__ == "__main__":
    main()
