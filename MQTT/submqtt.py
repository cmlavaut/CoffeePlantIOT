import paho.mqtt.client as mqtt

broker = "192.168.50.155"
topic = "prueba"
path = './csv/datos_new.csv'

def guardar(valorA, tabla):
    now = datetime.now()
    now_fecha = now.strftime("%d %m %y")
    now_hora = now.strftime("%H:%M:%S")
    try:
        tabla.insert(0, "Fecha", now_fecha)
        tabla.insert(1, "Hora", now_hora)
    except:
        #print("ya existe columnas de hora y fecha")
        pass            
    datos = [now_fecha, now_hora]
    datos = datos + valorA
    tabla.loc[tabla.shape[0]] = datos
    tabla.to_csv(path, index = False)
    

def on_connect(client, userdata, flags, rc):
    print("conectando al broker", rc)
    client.subscribe(topic)

def on_message(client, userdata, message, tabla):
    print("topic: {} y su mensaje es {}".format(message.topic, message.payload.decode())
    value = message.payload.decode()
    value = value.split()
    if (len(value) == 4):
        print("valores correctos")
        guardar(value, tabla)
    else:
        print("valores incorrectos")
        main()


def main():
    try:
        tabla = pd.read_csv(path)
    except:
        dicc = {
            "Place" : [],
            "humedad_suelo" : [],
            "humedad_amb" : [],
            "temperatura" :[],
        }
    tabla = pd.DataFrame.from_dict(dicc)
    tabla.to_csv(path,index= False)
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker)
    client.loop_forever()

