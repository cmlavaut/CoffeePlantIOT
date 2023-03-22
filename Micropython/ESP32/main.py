
#microcontrolador ESP32
import dht
from machine import Pin, ADC,UART
from time import sleep
import led_parpadeo
from umqtt.robust import MQTTClient
import machine
import network
import _thread

ssid = "N-47"
password = "@victor47"

broker = "192.168.50.168"
topic = "sensores/cuarto"

sensorHyT = dht.DHT22(Pin(27))
sensorHumedad = ADC(Pin(34))
sensorHumedad.atten(ADC.ATTN_11DB)
max_suelo = 54525
min_suelo = 22005
sensornivel = ADC(Pin(35))
sensornivel.atten(ADC.ATTN_11DB)
motor = Pin(23,Pin.OUT)
valor = 0
agua = 0

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

def regar():
    global sensornivel,motor,valor,agua
    while True:
        sleep(0.5)
        print(sensornivel.read_u16())
        if sensornivel.read_u16() < 401:
            motor.off()
            agua = 0
        elif valor < 50:
            motor.on()
            led_parpadeo.encendido(18)
            agua = 1
        else:
            motor.off()
            agua = 1
            led_parpadeo.encendido(19)
    
def mqttPublicar():
    global valor,sensorHumedad,agua,sensorHyT 
    while True:
        valor = (max_suelo - sensorHumedad.read_u16())*100/(max_suelo-min_suelo)
        sensorHyT.measure()
        temp =  sensorHyT.temperature()
        hum = sensorHyT.humidity()
        mensaje = "cuarto {} {} {} {}".format(valor,hum,temp,agua)
        print(mensaje)
        publicar_MQTT(mensaje)
        sleep(2)
        
connect_wifi()
_thread.start_new_thread(regar, ())
_thread.start_new_thread(mqttPublicar, ())
