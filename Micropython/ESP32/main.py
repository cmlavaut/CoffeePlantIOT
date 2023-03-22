#microcontrolador ESP32
import dht
from machine import Pin, ADC
from time import sleep
import led_parpadeo
from umqtt.robust import MQTTClient
import machine
import network
import uos
import _thread

ssid = "N-47"
password = "@victor47"

broker = "192.168.50.168"
topic = "sensores"

sensorHyT = dht.DHT22(Pin(27))
sensorHumedad = ADC(Pin(34))
sensorHumedad.atten(ADC.ATTN_11DB)
max_suelo = 54525
min_suelo = 22005
sensornivel = ADC(Pin(35))
sensornivel.atten(ADC.ATTN_11DB)
motor = Pin(23,Pin.OUT)
valorHumedad = 0
leerHumedad = open("humedad.txt", mode='r')
leerTiempo = open("tiempo.txt", mode='r')
humedadMinima = int(leerHumedad.read())
tiempo = int(leerTiempo.read())
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

def regar():
    global sensornivel,motor,valorHumedad,agua,humedadMinima,tiempo
    while True:
        sleep(0.5)
        valorHumedad = (max_suelo - sensorHumedad.read_u16())*100/(max_suelo-min_suelo)
        #print(sensornivel.read_u16())
        if sensornivel.read_u16() < 401:
            motor.off()
            agua = 0
        elif valorHumedad < humedadMinima:
            led_parpadeo.encendido(18)
            motor.on()
            sleep(tiempo)
            motor.off()
            sleep(0.5)
            agua = 1
        else:
            motor.off()
            agua = 1
            led_parpadeo.encendido(19)
            
            
def setHumedadMinima(topic, msg):
    global humedadMinima,tiempo
    if topic == b"control":
        try:
            humedadMinima = int(msg)
        except:
            datos = msg.decode().split(',')
            print(datos)
            humedadMinima = int(datos[0])
            tiempo = int(datos[1])
            with open("humedad.txt", "w") as f:
                f.write(datos[0])
            with open("tiempo.txt", "w") as f:
                f.write(datos[1])
            
def mqttPublicar():
    global valorHumedad,sensorHumedad,agua,sensorHyT, motor,humedadMinima,tiempo,sensornivel
    client = MQTTClient("esp32", broker)
    client.set_callback(setHumedadMinima)
    client.connect()
    client.subscribe(topic="control")
    while True:
        if not motor.value():
            sensorHyT.measure()
            temp =  sensorHyT.temperature()
            hum = sensorHyT.humidity()
            mensaje = "00 {} {} {} {} {} {}".format(valorHumedad,humedadMinima,tiempo,hum,temp, agua)
            print(mensaje)
        else :
            mensaje = "01 {} {} {} {}".format(valorHumedad,humedadMinima,tiempo,agua)
            print(mensaje)
        client.publish(topic, mensaje)
        client.check_msg()
        sleep(2)
        
connect_wifi()
_thread.start_new_thread(regar, ())
_thread.start_new_thread(mqttPublicar, ())
