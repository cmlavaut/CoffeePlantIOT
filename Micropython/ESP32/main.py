#microcontrolador ESP32
import dht
from machine import Pin, ADC,UART
from time import sleep
import led_parpadeo

sensor11 = dht.DHT11(Pin(27))
sensor = ADC(Pin(12))
sensor.atten(ADC.ATTN_11DB)
uart = UART(2,baudrate=115200)
max_suelo = 54525
min_suelo = 22005

while True:
    valor = (max_suelo - sensor.read_u16())*100/(max_suelo-min_suelo)
    if valor < 50:
        led_parpadeo.encendido(32)
    else:
        led_parpadeo.encendido(33)
    sensor11.measure()
    sensor11_temp =  sensor11.temperature()
    sensor11_hum = sensor11.humidity()
    print("cuarto {}% {}% {}C".format(valor,sensor11_hum,sensor11_temp))
    uart.write("cuarto {}% {}% {}C \n".format(valor,sensor11_hum, sensor11_temp))
    sleep(2)
    
    