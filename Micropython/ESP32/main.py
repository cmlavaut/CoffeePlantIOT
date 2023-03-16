
#microcontrolador ESP32
import dht
from machine import Pin, ADC,UART
from time import sleep
import led_parpadeo
from umqtt.robust import MQTTClient
import machine
import network

ssid = "N-47"
password = "@victor47"

broker = "192.168.50.168"
topic = "sensores/cuarto"

sensor22 = dht.DHT22(Pin(27))
sensor = ADC(Pin(34))
sensor.atten(ADC.ATTN_11DB)
max_suelo = 54525
min_suelo = 22005
sensornivel = Pin(4,Pin.IN)
motor = Pin(23,Pin.OUT)

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
    if not sensornivel.value():
        motor.off()
    elif valor < 50:
        motor.on()
        led_parpadeo.encendido(18)
    else:
        motor.off()
        led_parpadeo.encendido(19)
    sensor22.measure()
    sensor22_temp =  sensor22.temperature()
    sensor22_hum = sensor22.humidity()
    mensaje = "cuarto {} {} {}".format(valor,sensor22_hum,sensor22_temp)
    print(mensaje)
    publicar_MQTT(mensaje)
    sleep(2)
