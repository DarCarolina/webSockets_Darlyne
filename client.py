import network
import time
import machine import Pin,ADC
import usocket as socket
import ustruct as struct

# Configuración de la red Wi-Fi
SSID='TU_WIFI'
PASSWORD='TU_CONTRASEÑA'
SERVER_IP="192.168.20.53" #IP del servidor web
SERVER_PORT=8765

def connect_wifi():
    wlan=network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        print('Conectando a la red Wi-Fi...')
        time.sleep(1)
    print('Conexión Wi-Fi establecida:', wlan.ifconfig())

led=Pin(2,Pin.OUT) #Pin del LED
pot=ADC(Pin(34)) #Pin del potenciómetro
pot.atten(ADC.ATTN_11DB) #Rango de lectura del potenciómetro (0-3.3V)

from uwebsockets.client import connect #librería para WebSockets para conectarse al WIFI
connect_wifi()

try:
    with connect(f"ws://{SERVER_IP}:{SERVER_PORT}") as ws:
        print("Conectado al servidor NiceGUI")
        while True:
            val=pot.read() #lee el valor del potenciómetro
            ws.send(str(val)) #envía el valor del potenciómetro al servidor
            try:
                msg=ws.recv() #espera un mensaje del servidor
                if msg=="ON":
                    led.value(1) #enciende el LED
                elif msg=="OFF":
                    led.value(0) #apaga el LED
            except:
                pass #si no hay mensaje, continúa leyendo el potenciómetro
            time.sleep(0.1) #pequeña pausa para evitar saturar el servidor
except Exception as e:
    print("Error de conexión:", e)