from machine import Pin
from time import sleep

def encendido(pinled):
    led = Pin(pinled,Pin.OUT)
    led.on()
    sleep(0.2)
    
def apagado(pinled):
    led = Pin(pinled,Pin.OUT)
    led.off()
    sleep(0.2)