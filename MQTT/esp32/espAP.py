import network, ubinascii

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid="ESP-kmi") # establece el identificador de red -ESSID- 
ap.config(authmode=2, password="Caleidoscopio*")  # establece el modo de autentificación y la clave de red
ap.ifconfig(('10.10.10.1', '255.255.255.0', '10.10.10.1', '8.8.8.8'))
ap.config(max_clients=3)           # establece el número de clientes que se pueden conectar a la red
ap.config(channel=10)              # establece el canal 
ap.config(hidden=0)                # establece la visibilidad de la red

print('ESP32 configurado como AP')
print("ESSID:", ap.config('essid'))
print("Configuración de red (IP/netmask/gw/DNS):", ap.ifconfig())
