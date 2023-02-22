import dht
from machine import Pin, ADC,UART
from time import sleep
from led_parpadeo

s11 = dht.DHT11(Pin(27))
sensor = ADC(Pin(12))
    valor = (max_suelo - sensor.read_u16())*100/(max_suelo-min_suelo)
    if valor < 50:
        led_parpadeo.encendido(32)
    else:
        led_parpadeo.encendido(33)
    s11.measure()
    sensor11_temp =  s11.temperature()
    sensor11_hum = s11.humidity()
    print("maceta cuarto: {}% {}% {}C".format(valor,sensor11_hum,sensor11_temp))
    uart.write("maceta cuarto: {}% {}% {}C \n".format(valor,sensor11_hum, sensor11_temp))
    sleep(2)
    
    
