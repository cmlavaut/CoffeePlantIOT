import dht
from machine import Pin, ADC, UART
from time import sleep
import led
import _thread


#sensorbajo = Pin(14,Pin.IN, Pin.PULL_DOWN)
sensornivel = False
sensorHyT = dht.DHT22(Pin(6))
motor = Pin(18, Pin.OUT)
sensorHumedad = ADC(0)
uart = UART(1, baudrate=115200, tx=Pin(4), rx=Pin(5))
max_suelo = 21957
min_suelo = 11730
status = 0
value = 0

        
def regar():
    global sensornivel, status, value
    while True:
        sleep(0.5)
        #print (value)
        if sensornivel:
            status =1
            motor.off()
        elif value < 50:
            motor.on()
            led.encendido(20)
            led.apagado(21)
            status = 0
        else:
            motor.off()
            status = 0
            led.apagado(20)
            led.encendido(21)

_thread.start_new_thread(regar, ())
while True:
    #print(sensorHumedad.read_u16())
    value = (max_suelo - sensorHumedad.read_u16())*100/(max_suelo-min_suelo)
    sensorHyT.measure()
    temp =  sensorHyT.temperature()
    hum = sensorHyT.humidity()
    print("cuarto: {} {} {} {}".format(value, hum, temp, status))
    uart.write("cuarto {} {} {} {} \n".format(value,hum, temp, status))
    sleep(2)
  




