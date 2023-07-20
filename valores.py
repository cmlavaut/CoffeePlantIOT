import pandas as pd
import sys

path= "./csv/mediciones.csv"
place = int(sys.argv[1])
date= sys.argv[2]
parameter = sys.argv[3]
contador =0
lista_max= []
lista_min = []

dataframe= pd.read_csv(path)

while contador < 8:
    if parameter == "temperatura":
        datos = dataframe[(dataframe["Place"] == place) & (dataframe["Fecha"]== date)]
        data = datos["temperatura"]
        lista_max.append(data.max(skipna=True))
        lista_min.append(data.min(skipna=True))
        datelist=date.split()
        if int(date[0])< 32 and date[1]== "05":
            contador +=1
            date[0] = int(date[0]) +1
            date = ' '.join(datelist)
        else: 
            date[0] = "01"
            date[1] = "06"
            contador +=1
            date = ' '.join(datelist)
    elif parameter == "humedad ambiente":
        datos = dataframe[(dataframe["Place"] == place) & (dataframe["Fecha"]== date)]
        data = datos["humedad_amb"] 
        lista_max.append(data.max(skipna=True))
        lista_min.append(data.min(skipna=True))
        datelist=date.split()
        if int(date[0])< 32 and date[1]== "05":
            contador +=1
            date[0] = int(date[0]) +1
            date = ' '.join(datelist)
        else: 
            date[0] = "01"
            date[1] = "06"
            contador +=1
            date = ' '.join(datelist)
    elif parameter == "humedad suelo":
        datos = dataframe[(dataframe["Place"] == place) & (dataframe["Fecha"]== date)]
        data = dataframe["humedad_suelo"]
        lista_max.append(data.max(skipna=True))
        lista_min.append(data.min(skipna=True))
        datelist=date.split()
        if int(date[0])< 32 and date[1]== "05":
            contador +=1
            date[0] = int(date[0]) +1
            date = ' '.join(datelist)
        else: 
            date[0] = "01"
            date[1] = "06"
            contador +=1
            date = ' '.join(datelist)
    else:
        print("Parametro no establecido")



print("valores maximos")
print(lista_max)
print("valores minimos")
print(lista_min)
