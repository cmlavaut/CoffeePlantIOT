import serial
#import RPi.GPIO as gpio
import time
import sys
import pandas as pd
from datetime import datetime


dicc = {
        "humedad_sueloOut" : [],
        "humedad_ambOut" : [],
        "temperaturaOut" :[],
        }
tabla = pd.DataFrame.from_dict(dicc)
tabla.to_csv('./tabla.csv',index= False)

def main():
    arduino = serial.Serial()
    #arduino2= serial.Serial()
    try:
        puerto1= sys.argv[1]
        #puerto2= sys.argv[2]
        arduino.port= 'COM' + puerto1
        #arduino2.port = 'COM' + puerto2
        arduino.baudrate = 115200
        #arduino2.baudrate = 115200
        arduino.open()
        #arduino2.open()
    except:
        try:
            arduino.port = "/dev/ttyACM0"

            arduino.baudrate = 9600
            print(arduino.port)
            arduino.open()
        except:
            print("nothing conected")
            quit()
    
    while True:
        arduino.flushInput()
        sensor = arduino.readline()
        sensor = sensor.decode()
        value= sensor.split()
        value = value[2:5]
        print(value)
        guardar(value)
        time.sleep(3)
    arduino.close()
 





def guardar(valor):
        tabla = pd.read_csv('./tabla.csv')
        now = datetime.now()
        now_fecha = now.strftime("%d %m %y")
        now_hora = now.strftime("%H:%M:%S")
        try:
            tabla.insert(0, "Fecha", now_fecha)
            tabla.insert(1, "Hora", now_hora)
        except:
            print("ya existe columnas de hora y fecha")
            pass
        datos = [now_fecha, now_hora]
        datos.extend(valor)
        tabla.loc[tabla.shape[0]]= datos
        tabla.to_csv('./tabla.csv',index= False)


        """
        arduino2.flushInput()
        sensor11 = arduino2.readline()
                sensor11 = sensor11.decode()
        value11 = sensor11.split()
        if (len(value)==5 and len(value11)==5):
            print(" ".join(value[:2]))
            print("humedad suelo: " , value[2])
            print("humedad relativa: " , value[3])
            print("temperatura: " , value[4])
            print(" ")
            print(" ".join(value11[:2]))
            print("humedad suelo: ", value11[2])
            print("humedad relativa: ", value11[3])
            print("temperatura: ", value11[4])
            print(" ")
        else:
            print("valores incorrectos")
    
       
           """ 

if __name__ == "__main__":
    main()
