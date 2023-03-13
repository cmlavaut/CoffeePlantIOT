import machine
import network
from umqtt.robust import MQTTClient
import time
import dht
from machine import Pin, ADC,UART
import led_parpadeo

# Configuración de la conexión WiFi
WIFI_SSID = 'IZZI-41AF'
WIFI_PASSWORD = '50A5DC4F41AF'

# Configuración del broker MQTT
MQTT_BROKER = '192.168.0.2'
MQTT_TOPIC = 'sensores/sala'

#valores de sensor
s22 = dht.DHT22(Pin(12))
sensor = ADC(0)
max_suelo = 54525
min_suelo = 22005


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



# Conectarse al WiFi
connect_wifi()

# Publicar un mensaje MQTT
while True:
    valor = (max_suelo - sensor.read_u16())*100/(max_suelo-min_suelo)
    if valor < 50:
        led_parpadeo.encendido(4)
    else:
        led_parpadeo.encendido(5)
    s22.measure()
    sensor22_temp =  s22.temperature()
    sensor22_hum = s22.humidity()
    mensaje = "sala {} {} {}".format(valor,sensor22_hum,sensor22_temp)
    print(mensaje)
    #uart.write(mensaje)
    publish_mqtt(mensaje)
    time.sleep(2)

