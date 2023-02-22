#microcontrolador ESP32
import dht
from machine import Pin, ADC,UART
from time import sleep
import led_parpadeo

sensor22 = dht.DHT22(Pin(27))
sensor = ADC(Pin(14))
sensor.atten(ADC.ATTN_11DB)
uart = UART(2,baudrate=115200)
max_suelo = 54525
min_suelo = 22005

while True:
    valor = (max_suelo - sensor.read_u16())*100/(max_suelo-min_suelo)
    if valor < 50:
        led_parpadeo.encendido(25)
    else:
        led_parpadeo.encendido(26)
    sensor22.measure()
    sensor22_temp =  sensor22.temperature()
    sensor22_hum = sensor22.humidity()
    print("maceta cuarto: {}% {}% {}C".format(valor,sensor22_hum,sensor22_temp))
    uart.write("maceta cuarto: {}% {}% {}C \n".format(valor,sensor22_hum, sensor22_temp))
    sleep(2)
    
    