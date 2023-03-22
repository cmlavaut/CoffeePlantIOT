import machine
import network
from umqtt.robust import MQTTClient
import time
import dht
from machine import Pin, ADC,UART
import led_parpadeo
import uasyncio as asyncio

# Configuración de la conexión WiFi
WIFI_SSID = 'N-47'
WIFI_PASSWORD = '@victor47'
#WIFI_SSID = 'IZZI-41AF'
#WIFI_PASSWORD = '50A5DC4F41AF'

# Configuración del broker MQTT
MQTT_BROKER = '192.168.50.168'
MQTT_TOPIC = 'sensores'

#valores de sensor
sDTH = dht.DHT11(Pin(12))
sNivel = Pin(14,Pin.IN)
bomba = Pin(13,Pin.OUT)
sensor = ADC(0)
max_suelo = 54525
min_suelo = 22005
valorHumedad = 50
valor = 0


# Función para conectarse al WiFi
def connect_wifi(): 
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
        
    if not wlan.isconnected():
        print('Conectando al WiFi...')
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            pass
    print('Conexión WiFi establecida:', wlan.ifconfig())

# Función para publicar un mensaje MQTT
def publish_mqtt(message):
    client = MQTTClient("esp8266", MQTT_BROKER)
    client.connect()
    client.publish(MQTT_TOPIC, message)
    client.disconnect()

async def publicar():
    global valor
    while True:
        valor = (max_suelo - sensor.read_u16())*100/(max_suelo-min_suelo)
        sDTH.measure()
        temp =  sDTH.temperature()
        hum = sDTH.humidity()
        mensaje = "1 {} {} {}".format(valor,hum,temp)
        print(mensaje)
        publish_mqtt(mensaje)
        time.sleep(0.5)
        await asyncio.sleep(0.5)
async def regarPlantas():
    global sNivel, valor, valorHumedad
    print(sNivel.value())
    while True:
        if not sNivel.value():
            bomba.off()
            print("No hay suficiente agua")
            time.sleep(0.5)
        elif valor < valorHumedad:
            bomba.on()
            led_parpadeo.encendido(4)
            time.sleep(0.5)
        else:
            bomba.off()
            led_parpadeo.encendido(5)
            time.sleep(0.5)
        await asyncio.sleep(0.5)
# Conectarse al WiFi
connect_wifi()
loop = asyncio.get_event_loop()
loop.create_task(regarPlantas())
loop.create_task(publicar())
loop.run_forever()
