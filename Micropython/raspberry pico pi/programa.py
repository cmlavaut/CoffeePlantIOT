from time import sleep_ms, ticks_ms
from machine import I2C, Pin, ADC
from esp8266_i2c_lcd import I2cLcd
from DHT22 import DHT22

# The PCF8574 has a jumper selectable address: 0x20 - 0x27
DEFAULT_I2C_ADDR = 0x27
sensor = DHT22(Pin(15,Pin.IN,Pin.PULL_UP))



def avergaeAnalogRead(pinToRead):
    numberOfReadings = 8
    runningValue = 0
    
    for i in range(numberOfReadings):
        runningValue = runningValue + ADC(pinToRead).read_u16()
    runningValue = runningValue / numberOfReadings
    
    return runningValue

def mapFloat(x,in_min,in_max,out_min,out_max):
    return (x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min

def test_main():
    """Test function for verifying basic functionality."""
    print("Preparando lcd")
    i2c = I2C(0,scl=Pin(1), sda=Pin(0), freq=400000)
    lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 4, 20)
    sleep_ms(3000)
    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr("Sensores de Clima")

    while True:
        uvLevel = avergaeAnalogRead(0)
        refLevel = avergaeAnalogRead(1)
        outVoltage = 3.3 / refLevel * uvLevel
        uvIntensity = mapFloat(outVoltage,0.99,2.8,0.0,15.0)
        
        temp,hum = sensor.read()
        
        lcd.move_to(0, 1)
        lcd.putstr('Temperatura = {:3.1f} C'.format(temp))
        lcd.move_to(18, 1)
        lcd.putchar(chr(223))
        lcd.move_to(0, 2)
        lcd.putstr("Humedad= {:3.1f}%".format(hum))
        lcd.move_to(0, 3)
        lcd.putstr("Luz= {:3.1f}mW/cm^2".format(uvIntensity))
        sleep_ms(500)
#if __name__ == "__main__":
test_main()
