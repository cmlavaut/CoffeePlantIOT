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
broker = '192.168.50.155'
topic = 'sensores'


varHumedad = [0.0,0.0]
varTemperatura = [0.0,0.0]
varHumedadSuelo = [0.0,0.0]
agua = [0,0]

humedadMinima = [0,0]
tiempoRegado = [0,0]
cambiarPlanta = 0
numPlanta = 0

listoThread = [Thread(),Thread()]


app = Flask(__name__)

def on_connect(client,userdata,flags,rc):
    global topic
    print('Conectando al broker:',rc)
    print(topic)
    client.subscribe(topic)

def on_message(client,userdata,message):
    global varHumedad, varHumedadSuelo, varTemperatura, agua, humedadMinima,  tiempoRegado, cambiarPlanta, numPlanta 
    data = message.payload.decode().split()
    if len(data) == 7:
        if int(data[0]) == numPlanta:
            varHumedadSuelo[numPlanta] = np.round(float(data[1]), 2)
            humedadMinima[numPlanta] = int(data[2])
            tiempoRegado[numPlanta] = int(data[3])
            varHumedad[numPlanta] = np.round(float(data[4]),2)
            varTemperatura[numPlanta] = np.round(float(data[5]),2)
            agua[numPlanta] = int(data[6])
            print("Se cargo los datos")
    if cambiarPlanta:
        print("Se desconecto")
        client.disconnect()
    #print(data)
    #print('mensaje recibido el topic {}:{}'.format(message.topic,message.payload.decode()))

def conectarMQTT():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker)
    client.loop_forever()

def graficarVelocimetro(numPlanta):
    global varHumedadSuelo, varHumedad, varTemperatura, agua, humedadMinima, tiempoRegado

    figura_humedad = crear_velocimetro(varHumedad[numPlanta], 0, 100,'Humedad del Ambiente')
    figura_temperatura = crear_velocimetro(varTemperatura[numPlanta], 0, 50,'Temperatura del ambiente',suffix="°C")
    figura_humedad_suelo = crear_velocimetro(varHumedadSuelo[numPlanta], 0, 100,'Humedad Suelo')

    figura_temperatura.update_traces(gauge_bar_color="red")

    humedad = json.dumps(figura_humedad, cls=plotly.utils.PlotlyJSONEncoder)
    temp = json.dumps(figura_temperatura, cls=plotly.utils.PlotlyJSONEncoder)
    humedad_suelo = json.dumps(figura_humedad_suelo, cls=plotly.utils.PlotlyJSONEncoder)

    response = make_response([humedad,temp,humedad_suelo,agua[numPlanta],humedadMinima[numPlanta],tiempoRegado[numPlanta]])
    return response

def inicializarSensores(planta):
    global varHumedadSuelo, varHumedad, varTemperatura, agua, humedadMinima, tiempoRegado, topic, cambiarPlanta, numPlanta
    topic = 'sensores/{}'.format(planta)
    numPlanta = planta
    print(topic)
    cambiarPlanta = 0
    listoThread[numPlanta] = Thread(target=conectarMQTT)
    listoThread[numPlanta].start()
    context = {
        "varHumedad" : varHumedad,
        "varTemperatura" : varTemperatura,
        "varHumedadSuelo" : varHumedadSuelo,
        "agua" : agua,
        'humedadMinima' : humedadMinima,
        'tiempoRegado' : tiempoRegado,
        'numPlanta': numPlanta
    }
    return context


@app.route('/enviarData/<datos>',methods=['GET'])
def enviarData(datos):
    datoslist = datos.split(",")
    tipoSensor = datoslist.pop()
    datos = ",".join(datoslist)
    publish.single("control/{}".format(tipoSensor),datos,hostname=broker)
    time.sleep(1.0)
    response = make_response(json.dumps(datos))
    return response 


@app.route('/dataMqtt/<planta>',methods=['GET'])
def data0(planta):
    response = graficarVelocimetro(int(planta))
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
def main():
    global cambiarPlanta
    cambiarPlanta = 1
    return render_template('main.html')

@app.route('/sensor/<planta>',methods=['GET'])
def sensor(planta):
    context = inicializarSensores(int(planta))
    return render_template('sensor{}.html'.format(planta), **context)


if __name__ == '__main__':
    app.run(host='192.168.50.155',port=5000,debug=True)

