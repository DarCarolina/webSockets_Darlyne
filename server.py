#libreria
from nicegui import ui
import asyncio
import websockets
import threading #procesos

#Array['0(esto es según el índice)','off']
#Biblioteca{pot value(es la clave)}
data = {'pot_value':  '0','led_status': 'OFF'}
esp32_socket = None

async def ws_server_logic(websocket, path): #parámetros entre el cliente y el servidor
    global esp32_socket
    esp32_socket = websocket #esta variable va a guardar la comunicación entre el cliente y servidor
    print("ESP32 conectado")
    try:
        async for message in websocket: #función asincrona a la espera de mensajes del cliente
            #recibir la informacion de un potenciómetro
            data['pot_value'] = message
            ui_update.refresh() #decorador para actualizar la interfaz
    except websockets.exceptions.ConnectionClosed:
        print("ESP32 desconectado")
    finally:
        esp32_socket = None

#INICIALIZA EL SERVIDOR WEB
def start_ws_thread():
    loop=asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    start_server = websockets.serve(ws_server_logic, "0.0.0.0", 8765) #dirección IP y puerto(servicio específico al que se conecta)
    loop.run_until_complete(start_server)
    loop.run_forever()

threading.Thread(target=start_ws_thread, daemon=True).start() #pasa la función como objetivo de iniciar

def toggle_led():
    if esp32_socket:
        new_status = 'ON' if data['led_status'] == 'OFF' else 'OFF'
        data['led_status'] = new_status

@ui.refreshable #decorador para actualizar la interfaz (solo un espacio de la página)
def ui_update():
    with ui.card().classes('items-center p-4 m-2'):
        ui.label(f'Potenciómetro: {data["pot_value"]}').classes('text-h3')

        #representación visual de potenciómetro
        val=int(data['pot_value']) if data['pot_value'. isdigit() selse 0] #condicional
        ui.knob(value=val, min=0, max=4095, show_value=True).classes('m-4')

        #led
        ui.label(f'LED: {data["led_status"]}').classes('text-h3')
        ui.button('Cambiar estado del LED', on_click=toggle_led).props ('elevated').classes('m-4')
@ui.page('/')
def index():
    ui.label('Dashboard ESP32').classes('text-h2 m-4')
    ui_update() #llama a la función para mostrar la interfaz
ui.run(host='0.0.0.0', port=8080, title='ESP32 Dashboard') #ejecuta el servidor web en todas las interfaces de red, puerto 8080
    
