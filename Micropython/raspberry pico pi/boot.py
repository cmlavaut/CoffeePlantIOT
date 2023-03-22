# boot.py para la Raspberry Pi Pico

# Importar módulos necesarios
import machine
import time

# Configuración de pines de E/S
led = machine.Pin(18, machine.Pin.OUT)

# Encender el LED
led.value(1)

# Esperar 1 segundo
time.sleep(1)

# Apagar el LED
led.value(0)

# Ejecutar el archivo main.py
exec(open('main.py').read())
