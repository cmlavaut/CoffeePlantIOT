from machine import Pin, ADC
from time import sleep

sensorbajo = Pin(14,Pin.IN, Pin.PULL_DOWN)
motor = Pin(22, Pin.OUT)
sensorHumedad = ADC(26)
max_suelo = 54525
min_suelo = 22005

while True:
    valor = (max_suelo - sensorHumedad.read_u16())*100/(max_suelo-min_suelo)
    print(valor)
    while valor < 50:
        if sensorbajo.value() == 1:
            motor.on()
            sleep(0.5)
        else:
            motor.off()
            print("poco nivel de agua")
            sleep(0.5)
            break
    
    print ("llenar agua xfavor")
    print(valor)
    sleep(1)



        
