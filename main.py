import time
import threading
import asyncio
from settings.configLoad import ConfigLoader
from Stream.streamingServer import Stream
from UART.uart import *
from GPIO.gpio import *

# --------------------  Einstellungen laden  -------------------- #
config = ConfigLoader("settings/config.json")
IP = config.get("ip")
PORT_INTERFACE = config.get("port_Interface")
PORT_STREAM = config.get("port_Stream")
PORT_UART = config.get("port_UART")

# --------------------  Stream  -------------------- #
stream = Stream(IP, PORT_STREAM)

# --------------------  UART-Interface  -------------------- #
BAUDRATE = 115200
SERIAL_PORT = "/dev/ttyS0"
Esp32_UART = SerialInterface(SerialPort=SERIAL_PORT, Baudrate=BAUDRATE)

# --------------------  UART-Daten & Synchronisation  -------------------- #
dataArray = [255, 255, 255, 255]
data_lock = threading.Lock()

def update_data(val0, val1, val2, val3):
    global dataArray
    with data_lock:
        dataArray[0] = val0 % 256
        dataArray[1] = val1 % 256
        dataArray[2] = val2 % 256
        dataArray[3] = val3 % 256

def send_data_thread(serial_interface):
    while True:
        with data_lock:
            serial_interface.sendData(dataArray)
        time.sleep(0.1)

# --------------------  WebSocket-Server in eigenem Thread  -------------------- #
def getDataWebsocket(a, b, c, d):
    return [a, b, c, d]

server = SerialInterfaceWebsocket(serial_interface=Esp32_UART, ip=IP, port=8765, update_callback=getDataWebsocket)

def start_websocket_server():
    ws_server = SerialInterfaceWebsocket(Esp32_UART, IP, PORT_UART)
    asyncio.run(ws_server.start_server())

# --------------------  Threads erstellen  -------------------- #
stream_thread = threading.Thread(target=stream.start, daemon=True)
send_thread = threading.Thread(target=send_data_thread, args=(Esp32_UART,), daemon=True)
ws_thread = threading.Thread(target=start_websocket_server, daemon=True)

# --------------------  GPIO settings  -------------------- #
esp32_resetter = ESP32Resetter(reset_pin=17)  # Erstelle eine Instanz der Klasse




# --------------------  Main  -------------------- #
if __name__ == "__main__":
    print(f"IP: {IP}, WebSocket Port: {PORT_INTERFACE}, Stream Port: {PORT_STREAM}, UART Port: {PORT_UART}")    
    i = 0
    received_ip = None
    while received_ip is None:
        i = i + 1
        if (i > 6):
            i = 0
            print("III")
            esp32_resetter.reset()
        print("Warte auf gültige IP...")
        time.sleep(1)
        received_ip = Esp32_UART.initial(IP)
    
    print(f"ESP32 hat folgende IP bestätigt: {received_ip}")
    
    stream_thread.start()
    send_thread.start()
    ws_thread.start()

    asyncio.run(server.start_server())

    try:
        # Beispiel: Periodische Aktualisierung der Daten (Werte von 0 bis 255)
        # for i in range(256):
        #     update_data(i, i, i, i)
        #     time.sleep(0.1)
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nBeenden...")
