from flask import Flask, render_template, make_response, request, url_for,redirect
import numpy as np
import pandas as pd
import os
import time
import json
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from threading import Thread
import matplotlib.pyplot as plt
import plotly.utils
from velocimetro import crear_velocimetro
from graficar import *


path= "./csv/mediciones.csv"
pathCredenciales = "./credenciales/credenciales.json"
broker = '192.168.50.155'
topic = 'sensores'

leerCredenciales = open(pathCredenciales)
credenciales = json.load(leerCredenciales)
user = credenciales['user']
passwd = credenciales['passwd']

humSuelo= 0.0
humMinina= 0.0
humAmbiente= 0.0
tiempoRegado = 0.0
temperatura=0.0
aguaStatus = 0
idplanta = 0
listoThread = [Thread(),Thread(),Thread(),Thread()]

app = Flask(__name__)


def on_connect(client,userdata,flags,rc):
    global topic
    print('Conectando al broker:',rc)
    print(topic)
    client.subscribe(topic)

def on_message(client,userdata,message):
    global humSuelo, humMinina, humAmbiente, tiempoRegado, temperatura, aguaStatus, idplanta
    data = message.payload.decode().split()
    if len(data) == 7:
        print('datos correctos')
        #if int(data[0]) == idplanta:
        humSuelo = float(data[1])
        humMinina = float(data[2])
        tiempoRegado = int(data[3])
        humAmbiente = float(data[4])
        temperatura = float(data[5])
        aguaStatus = int(data[6])
        print("datos cargados")
    print(data)
    print('mensaje recibido el topic {}:{}'.format(message.topic,message.payload.decode()))

def conectarMQTT():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(user,passwd)
    client.connect(broker)
    client.loop_forever()


@app.route('/graficas')
def graficas():
    dataFrame = pd.read_csv(path)
    fechaArray = dataFrame.loc[:,'Fecha'].drop_duplicates().dropna().to_numpy()
    lenFecha = len(fechaArray)
    content = {
        'fechaArray' : fechaArray,
        'lenFecha' : lenFecha
    }
    return render_template("graficas.html", **content)


def graficarVelocimetro():
    global humAmbiente, humSuelo, humMinina, tiempoRegado, temperatura, aguaStatus

    figura_humedad = crear_velocimetro(humAmbiente[idplanta], 100,'Humedad del Ambiente')
    figura_temperatura = crear_velocimetro(temperatura[idplanta], 50,'Temperatura del ambiente',suffix="°C")
    figura_humedad_suelo = crear_velocimetro(humSuelo[idplanta], 100,'Humedad Suelo')

    figura_temperatura.update_traces(gauge_bar_color="red")

    humedad = json.dumps(figura_humedad, cls=plotly.utils.PlotlyJSONEncoder)
    temp = json.dumps(figura_temperatura, cls=plotly.utils.PlotlyJSONEncoder)
    humedad_suelo = json.dumps(figura_humedad_suelo, cls=plotly.utils.PlotlyJSONEncoder)

    response = make_response(humedad, temp, humedad_suelo, aguaStatus[idplanta],humMinina[idplanta],tiempoRegado)
    return response


@app.route('/visualizar/<planta>')
def visualizar(planta):
    global humMinina, humAmbiente, humSuelo, temperatura, aguaStatus, tiempoRegado, topic
    topic = 'sensores/{}'.format(planta)
    idplanta = int(planta)
    listoThread[idplanta] = Thread(target=conectarMQTT)
    listoThread[idplanta].start()
    context= {
        "humSuelo" : humSuelo,
        "humAmbiente": humAmbiente,
        "humMinima": humMinina,
        "temperatura": temperatura,
        "aguaStatus": aguaStatus,
        "tiempoRegado": tiempoRegado
    }
    return render_template("visualizar.html", **context)


@app.route('/enviarData/<datos>',methods=['GET'])
def enviarData(datos):
    publish.single("control",datos,hostname=broker)
    time.sleep(1.0)
    response = make_response(json.dumps(datos))
    return response 

@app.route('/dataMqtt/',methods=['GET'])
def dataMqtt():
    global humMinina, humAmbiente, humSuelo, temperatura, aguaStatus, tiempoRegado, topic
    dato = [tiempoRegado,humMinina, humAmbiente, humSuelo, temperatura, aguaStatus, topic]
    print(dato)
    response = make_response(json.dumps(dato))
    return response 

@app.route('/datos/', methods=['GET'])
def datos():
    lugar = request.cookies.get("lugar")
    parametro = request.cookies.get("parametro")
    fecha = request.cookies.get("fecha")
    dato = '{} {} {}'.format(lugar, parametro, fecha)
    generar = 'python graficar.py "{}" "{}" "{}"'.format(lugar, fecha, parametro)
    print(generar)
    os.system(generar)
    return generar

@app.route("/")
def home():
    #poner disconnet mqtt y matar los hilos
    return  render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True, port=5010)