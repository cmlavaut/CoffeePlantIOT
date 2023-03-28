import paho.mqtt.client as mqtt
import sys

broker = "192.168.0.20"


def on_message(client, userdata, message):
    print(message.topic, str(message.payload.decode("utf-8")))

def main():
    client = mqtt.Client()
    client.on_message = on_message
    topic = sys.argv[1]
    client.connect(broker, 1883)
    client.subscribe(topic)
    client.loop_forever()


if __name__ == "__main__":
    main()
