import serial
import time
import sys
import pandas as pd
from datetime import datetime


dicc = {
        "Place" : [],
        "humedad_suelo" : [],
        "humedad_amb" : [],
        "temperatura" :[],
        }
tabla = pd.DataFrame.from_dict(dicc)
tabla.to_csv('./datos.csv',index= False)

def main():
    arduino = serial.Serial()
    arduino2= serial.Serial()
    try:
        puerto1= sys.argv[1]
        puerto2= sys.argv[2]
        arduino.port= 'COM' + puerto1
        arduino2.port = 'COM' + puerto2
        arduino.baudrate = 115200
        arduino2.baudrate = 115200
        arduino.open()
        arduino2.open()
    except:
        try:
            #puerto1 = sys.argv[1]
            #puerto2 = sys.argv[2]
            arduino.port = "/dev/ttyUSB0" 
            arduino2.port = "/dev/ttyUSB1"
            arduino.baudrate = 115200
            arduino2.baudrate = 115200
            arduino.open()
            arduino2.open()
        except:
            print("nothing conected")
            quit()
    
    while True:
        arduino.flushInput()
        sensor = arduino.readline()
        sensor = sensor.decode()
        value= sensor.split()
        arduino2.flushInput()
        sensor11 = arduino2.readline()
        sensor11 = sensor11.decode()
        value11 = sensor11.split()
        if (len(value)==4 and len(value11)==4):
            print("valores correctos")
            guardar(value, value11)
            print(tabla)
        else:
            print("valores incorrectos")
        
        time.sleep(3)
    arduino.close()
 



def guardar(valorA, valorB):
        tabla = pd.read_csv('./datos.csv')
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
        for i in range(len(valorA)):
            datos.append(valorA[i])
        for k in range(len(valorB)):
            datos.append(valorB[k])
        #print(tabla)
        #print(datos)
        tabla.loc[tabla.shape[0]]= datos
        tabla.to_csv('./datos.csv',index= False)
        return tabla

if __name__ == "__main__":
    main()
