import pandas as pd
import matplotlib.pyplot as plt

def main():
    datos = pd.read_csv("./datos.csv")
    sala = datos[(datos["Place"]=="sala")&(datos["Fecha"]=="26 02 23")].reset_index(drop=True)
    sala = sala.loc[:,["Hora", "temperatura"]]
    contador = 0
    for temp in sala.loc[:,"temperatura"]:
        sala.loc[contador,"temperatura"] = float(temp[:-1])
        contador += 1 
    print("valor max")
    valor = sala.loc[:,"temperatura"].max()
    print(sala[sala["temperatura"] == valor])
    

    print("valor min")
    valor = sala.loc[:,"temperatura"].min()
    print(sala[sala["temperatura"] == valor])

    sala = sala[sala["temperatura"] < 35] 
    print(sala)
    sala.plot(x= "Hora", y= "temperatura")
    plt.show()

if __name__ == "__main__":
    main()





