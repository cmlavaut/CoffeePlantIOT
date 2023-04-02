from flask import Flask, render_template, make_response
import plotly.utils
from velocimetro import crear_velocimetro
import matplotlib.pyplot as plt
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from threading import Thread
import numpy as np
import pandas as pd
import time
import json
import os

path = './csv/baseDatos.csv'
broker = '192.168.50.168'
topic = 'sensores'


varHumedad = 0.0
varTemperatura = 0.0
varHumedadSuelo = 0.0
agua = 0

humedadMinima = 0
tiempoRegado = 0

app = Flask(__name__)

def on_connect(client,userdata,flags,rc):
    print('Conectando al broker:',rc)
    client.subscribe(topic)

def on_message(client,userdata,message):
    global varHumedad, varHumedadSuelo, varTemperatura, agua, humedadMinima,  tiempoRegado 
    data = message.payload.decode().split()
    if len(data) == 7:
        varHumedadSuelo = np.round(float(data[1]), 2)
        humedadMinima = int(data[2])
        tiempoRegado = int(data[3])
        varHumedad = np.round(float(data[4]),2)
        varTemperatura = np.round(float(data[5]),2)
        agua = int(data[6])
    #print(data)
    #print('mensaje recibido el topic {}:{}'.format(message.topic,message.payload.decode()))

def conectarMQTT():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker)
    client.loop_forever()

@app.route('/enviarData/<datos>',methods=['GET'])
def enviarData(datos):
    publish.single("control",datos,hostname=broker)
    time.sleep(1.0)
    response = make_response(json.dumps(datos))
    return response 


@app.route('/dataMqtt',methods=['GET'])
def data():
    global varHumedadSuelo, varHumedad, varTemperatura, agua, humedadMinima, tiempoRegado

    figura_humedad = crear_velocimetro(varHumedad, 0, 100,'Humedad del Ambiente')
    figura_temperatura = crear_velocimetro(varTemperatura, 0, 50,'Temperatura del ambiente',suffix="°C")
    figura_humedad_suelo = crear_velocimetro(varHumedadSuelo, 0, 100,'Humedad Suelo')

    figura_temperatura.update_traces(gauge_bar_color="red")

    humedad = json.dumps(figura_humedad, cls=plotly.utils.PlotlyJSONEncoder)
    temp = json.dumps(figura_temperatura, cls=plotly.utils.PlotlyJSONEncoder)
    humedad_suelo = json.dumps(figura_humedad_suelo, cls=plotly.utils.PlotlyJSONEncoder)

    response = make_response([humedad,temp,humedad_suelo,agua,humedadMinima,tiempoRegado])
    return response

@app.route('/graficar/<parametro>',methods=['GET'])
def graficar(parametro):
    datosGraficar = parametro.split(',')
    generarGrafico = 'python graficar.py "cuarto" "{}" "{}"'.format(datosGraficar[1],datosGraficar[0])
    #print(generarGrafico)
    os.system(generarGrafico)
    response = make_response(generarGrafico)
    return response

@app.route('/historial')
def historial():
    dataFrame = pd.read_csv(path)
    fechaArray = dataFrame.loc[:,'Fecha'].drop_duplicates().to_numpy()
    lenFecha = len(fechaArray)
    content = {
        'fechaArray' : fechaArray,
        'lenFecha' : lenFecha
    }
    return render_template("historial.html", **content)

@app.route('/')
def index():
    global varHumedadSuelo, varHumedad, varTemperatura, agua, humedadMinima, tiempoRegado
    threadMqtt = Thread(target=conectarMQTT)
    threadMqtt.start()
    context = {
        "varHumedad" : varHumedad,
        "varTemperatura" : varTemperatura,
        "varHumedadSuelo" : varHumedadSuelo,
        "agua" : agua,
        'humedadMinima' : humedadMinima,
        'tiempoRegado' : tiempoRegado
    }
    return render_template('index.html', **context)

if __name__ == '__main__':
    app.run(host="192.168.50.247",port=5000,debug=True)

