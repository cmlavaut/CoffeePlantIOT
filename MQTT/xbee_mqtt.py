import serial 
import paho.mqtt.client as mqtt


ser = serial.Serial('/dev/ttyUSB1', 115200)
client = mqtt.Client()
client.connect('192.168.0.20', 1883)

while True:
    data = ser.readline().strip()
    print(data)
    client.publish('datos/xbee', data)



