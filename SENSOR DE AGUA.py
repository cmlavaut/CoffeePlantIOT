from machine import Pin
from time import sleep

sensorbajo = Pin(14,Pin.IN, Pin.PULL_DOWN)
led = Pin(22, Pin.OUT)


while True:
    if sensorbajo.value() == 1:
        led.on()
        sleep(0.5)
    else:
        led.off()
        print("poco nivel de agua")
        sleep(0.5)
        

