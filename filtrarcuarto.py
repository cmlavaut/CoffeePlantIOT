import pandas as pd
import matplotlib.pyplot as plt
import sys

path = "./csv/datos_new.csv"

def main():
    place = sys.argv[1]
    date = sys.argv[2]
    columna = sys.argv[3]
    datos = pd.read_csv(path)
    cuarto = datos[(datos["Place"]== place )&(datos["Fecha"]== date)].reset_index(drop=True)
    cuarto = cuarto.loc[:,["Hora", columna]]
    
    contador = 0
    for index, row in cuarto.iterrows():
        cuarto.loc[contador,columna] = float(row[columna][:])
        print(row[columna])
        contador += 1 
    print("valor max")
    valor = cuarto.loc[:, columna].max()
    print(cuarto[cuarto[columna] == valor])
    
    
if __name__ == "__main__":
    main()





