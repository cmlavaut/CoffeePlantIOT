#microcontrolador ESP32
import dht
from machine import Pin, ADC,UART
from time import sleep
import led_parpadeo
from umqtt.robust import MQTTClient
import machine
import network

ssid = "IZZI-41AF"
password = "50A5DC4F41AF"

broker = "192.168.0.2"
topic = "sensores/cuarto"

sensor11 = dht.DHT11(Pin(27))
sensor = ADC(Pin(36))
sensor.atten(ADC.ATTN_11DB)
#uart = UART(2,baudrate=115200)
max_suelo = 54525
min_suelo = 22005

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("por favor conectar")
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print("conexion establecida: ", wlan.ifconfig())

def publicar_MQTT(mensaje):
    client = MQTTClient("esp32", broker)
    client.connect()
    client.publish(topic, mensaje)
    client.disconnect()
    
connect_wifi()
while True:
    valor = (max_suelo - sensor.read_u16())*100/(max_suelo-min_suelo)
    if valor < 50:
        led_parpadeo.encendido(32)
    else:
        led_parpadeo.encendido(33)
    sensor11.measure()
    sensor11_temp =  sensor11.temperature()
    sensor11_hum = sensor11.humidity()
    mensaje = "cuarto {} {} {}".format(valor,sensor11_hum,sensor11_temp)
    print(mensaje)
    #uart.write(mensaje)
    publicar_MQTT(mensaje)
    sleep(2)
    
    
