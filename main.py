import time
import threading
from settings.configLoad import ConfigLoader
from Stream.streamingServer import Stream
from UART.uart import *

# --------------------  Load settings  -------------------- #
config = ConfigLoader("settings/config.json")
IP = config.get("ip")
PORT_INTERFACE = config.get("port_Interface")
PORT_STREAM = config.get("port_Stream")
PORT_UART = config.get("port_UART")

# --------------------  Stream  -------------------- #
stream = Stream(IP, PORT_STREAM)

# --------------------  UART interface  -------------------- #
SERIAL_PORT = "/dev/ttyS0"
Esp32_UART = SerialInterface(SerialPort=SERIAL_PORT, Baudrate=BAUDRATE)

# --------------------  UART Data  -------------------- #
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


# --------------------  Threads erstellen  -------------------- #
stream_thread = threading.Thread(target=stream.start, daemon=True)
send_thread = threading.Thread(target=send_data_thread, args=(Esp32_UART,), daemon=True)

# --------------------  Main  -------------------- #
if __name__ == "__main__":
    print(f"IP: {IP}, Webpage Port: {PORT_INTERFACE}, Stream: {PORT_STREAM}, UART Port: {PORT_UART}")

    received_ip = Esp32_UART.initial(IP)
    print(f"ESP32 hat folgende IP bestätigt: {received_ip}")
    time.sleep(2)

    # Starte Threads
    stream_thread.start()
    send_thread.start()

    try:
        for i in range(256):
            update_data(i, i, i, i)
            time.sleep(0.1)

        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nBeenden...")
