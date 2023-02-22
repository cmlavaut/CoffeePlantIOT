#microcontrolador ESP32
import dht
from machine import Pin, ADC,UART
from time import sleep

sensor11 = dht.DHT11(Pin(27))
#sensor22 = dht.DHT22(Pin(26))
sensor = ADC(Pin(12))
sensor.atten(ADC.ATTN_11DB)
uart = UART(2,baudrate=115200)


while True:
    valor = sensor.read_u16()
    print(valor)
    sensor11.measure()
    sensor11_temp =  sensor11.temperature()
    sensor11_hum = sensor11.humidity()
    print("temp amb: {} C y humedad relativa {} %".format(sensor11_temp,sensor11_hum))
    sensor22.measure()
    sensor22_temp =  sensor22.temperature()
    sensor22_hum = sensor22.humidity()
    print("temp amb: {} C y humedad relativa {} %".format(sensor22_temp, sensor22_hum))
    uart.write("{},{},{},{},{}\n".format(valor,sensor11_temp, sensor11_hum,sensor22_temp, sensor22_hum) )
    sleep(2)
    
    
