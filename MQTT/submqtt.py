import paho.mqtt.client as mqtt

broker = "192.168.50.155"
topic = "prueba"
path = './csv/datos_new.csv'

def guardar(valorA, tabla):
    now = datetime.now()
    now_fecha = now.strftime("%d %m %y")
    now_hora = now.strftime("%H:%M:%S")
    
    


def on_connect(client, userdata, flags, rc):
    print("conectando al broker", rc)
    client.subscribe(topic)

def on_message(client, userdata, message):
    print("topic: {} y su mensaje es {}".format(message.topic, message.payload.decode()))



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker)
client.loop_forever()

