import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys

path = "./csv/mediciones.csv"
hora_arreglo = np.arange(0,24)
humedadamb = np.empty(0)
humedadsuelo = np.empty(0)
humedadsuelo = np.empty(0)
temperatura = np.empty(0)


def promedio(columna,i , sala):
    hora = sala[sala["Hora"].astype(int)==i]
    hora = hora.loc[:, columna].astype(float)
    h_arr = hora.to_numpy()
    return np.round(np.mean(h_arr),3)


def graficar(x,y,variable,titulo):
    plt.plot(x, y, "r", marker = "o")
    plt.title(titulo)
    plt.xlabel("Horas")
    plt.ylabel(variable)
    titulo = titulo.replace(" ","")
    titulo = titulo.replace(":","")
    plt.savefig('./static/graficos/{}.png'.format(titulo))
    #plt.show()


def main():
    global humedadamb, humedadsuelo, temperatura
    datos = pd.read_csv(path)
    place = sys.argv[1]
    fecha = sys.argv[2]
    variable = sys.argv[3]
    placenew = '0'+place

    sala = datos[(datos["Place"]== placenew)&(datos["Fecha"]== fecha)].reset_index(drop=True)
    print(sala)

    for index, row in sala.iterrows():
        sala.loc[index,"Hora"] = row["Hora"][:-6]

    print(sala.tail(8)) 

    for i in hora_arreglo:
        h_mediana = promedio("humedad_amb", i, sala)
        humedadamb = np.append(humedadamb, h_mediana)
        h_mediana = promedio("humedad_suelo", i, sala)
        humedadsuelo = np.append(humedadsuelo, h_mediana)
        h_mediana = promedio("temperatura", i, sala)
        temperatura = np.append(temperatura, h_mediana)

    if variable == 'temperatura':
        y = temperatura
    elif variable == 'humedad ambiente':
        y = humedadamb
    else:
        y = humedadsuelo


    print(hora_arreglo)
    print(humedadamb)
    print(humedadsuelo)
    titulo = "Sensor:{} Fecha:{}".format(variable,fecha)
    graficar(hora_arreglo,y,variable,titulo)




if __name__ == "__main__":
    main()