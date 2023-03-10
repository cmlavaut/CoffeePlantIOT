<<<<<<< HEAD
import pandas as pd
import matplotlib.pyplot as plt
import sys

path = "./csv/datos.csv"

def main():
    place = sys.argv[1]
    date = sys.argv[2]
    parametro1 = sys.argv[3]
    datos = pd.read_csv(path)
    cuarto = datos[(datos["Place"]== place )&(datos["Fecha"]== date)].reset_index(drop=True)
    cuarto = cuarto.loc[:,["Hora", parametro1]]
    contador = 0
    for index, row in cuarto.iterrows():
        cuarto.loc[contador,parametro1] = float(row[parametro1][:-1])
        contador += 1 
    print("valor max")
    valor = cuarto.loc[:, parametro1].max()
    print(cuarto[cuarto[parametro1] == valor])
    

    cuarto.plot(x= "Hora", y= parametro1)
    plt.show()

if __name__ == "__main__":
    main()





=======
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





>>>>>>> 47d1aa097eecb4eca84d4ed3c5eccb66f2ac0ae0
