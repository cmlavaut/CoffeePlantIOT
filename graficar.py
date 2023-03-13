import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

path = "./csv/datos.csv"
hora_arreglo = np.arange(0,24)
humedadamb = np.empty(0)
humedadsuelo = np.empty(0)


def promedio(columna,i , sala):
    hora = sala[sala["Hora"].astype(int)==i]
    hora = hora.loc[:, columna].astype(float)
    h_arr = hora.to_numpy()
    return np.round(np.mean(h_arr),3)
    
    


def main():
    global humedadamb, humedadsuelo
    datos = pd.read_csv(path)
    sala = datos[(datos["Place"]=="sala")&(datos["Fecha"]=="27 02 23")].reset_index(drop=True)
        
    
    for index, row in sala.iterrows():
        sala.loc[index,"humedad_amb"] = row["humedad_amb"][:-1]
        sala.loc[index,"humedad_suelo"] = row["humedad_suelo"][:-1]
        sala.loc[index,"Hora"] = row["Hora"][:-6]
    
    print(sala.tail(8)) #muestra los ultimos 8 filas

    for i in hora_arreglo:
        h_mediana = promedio("humedad_amb", i, sala)
        humedadamb = np.append(humedadamb, h_mediana)
        h_mediana = promedio("humedad_suelo", i, sala)
        humedadsuelo = np.append(humedadsuelo, h_mediana)
         
    print(hora_arreglo)
    print(humedadamb)
    print(humedadsuelo)
        
    plt.plot(hora_arreglo, humedadamb)
    plt.plot(hora_arreglo, humedadsuelo)
    plt.show()

if __name__ == "__main__":
    main()





