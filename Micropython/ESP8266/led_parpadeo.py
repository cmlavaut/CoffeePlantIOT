from machine import Pin
from time import sleep

def encendido(pinled):
    led = Pin(pinled,Pin.OUT)
    for i in range(5):
        led.on()
        sleep(0.2)
        led.off()
        sleep(0.2)
    
