import pandas as pd
import matplotlib.pyplot as plt

def main():
    datos = pd.read_csv("./datos.csv")
    cuarto = datos[(datos["Place"]=="cuarto")&(datos["Fecha"]=="26 02 23")].reset_index(drop=True)
    cuarto = cuarto.loc[:,["Hora", "humedad_suelo", "humedad_amb"]]
    contador = 0
    for index, row in cuarto.iterrows():
        cuarto.loc[contador,"humedad_suelo"] = float(row["humedad_suelo"][:-1])
        cuarto.loc[contador,"humedad_amb"] = float(row["humedad_amb"][:-1])
        contador += 1 
    print("valor max")
    valor = cuarto.loc[:,"humedad_suelo"].max()
    print(cuarto[cuarto["humedad_suelo"] == valor])
    

    print("valor min")
    valor = cuarto.loc[:,"humedad_suelo"].min()
    print(cuarto[cuarto["humedad_suelo"] == valor])
     
    #sala = sala[sala["temperatura"] < 35] 
    #print(sala)
    #cuarto.plot(x= "Hora", y1= "humedad_suelo", y2 = "humedad_amb")
    cuarto.plot(x= "Hora", y= "humedad_amb")
    plt.show()

if __name__ == "__main__":
    main()





