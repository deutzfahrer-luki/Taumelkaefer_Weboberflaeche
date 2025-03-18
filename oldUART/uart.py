import serial
import time
import asyncio
import websockets
from GPIO.gpio import *

class SerialInterface:
    def __init__(self, SerialPort, Baudrate):
        self.esp32_resetter = ESP32Resetter(reset_pin=17)  # Erstelle eine Instanz der Klasse
        self.serialPort = SerialPort
        self.baudrate = Baudrate

        try:
            self.serial = serial.Serial(self.serialPort, self.baudrate, timeout=1)
            print(f"Connection established on {self.serialPort} with baudrate {self.baudrate}")
            time.sleep(2)
        except serial.SerialException as e:
            print(f"Error initializing serial port: {e}")
            self.serial = None
        
        
    def initial(self, ip, timeout=10, delay=1):
        start_time = time.time()
        self.ipencoded = ip.encode()

        while time.time() - start_time < timeout:
            # IP erneut senden, solange keine Antwort kommt
            self.serial.write(self.ipencoded)  
            self.serial.flush()
            self.esp32_resetter.reset()

            print(f"Initial UART Send to Start the ESP32 on {ip}")

            # Warte auf Antwort
            wait_start = time.time()
            while time.time() - wait_start < 0.5:
                if self.serial.in_waiting:  # Prüft, ob Daten verfügbar sind
                    received_ip = self.serial.read(len(self.ipencoded))
                    if received_ip == self.ipencoded:
                        print(f"ESP32 antwortet mit der gleichen IP: {ip}")
                        return ip  # Gibt die IP zurück, wenn sie übereinstimmt

                time.sleep(delay)

        print("Timeout erreicht. Keine Antwort vom ESP32 erhalten.")
        return None  # Falls keine Antwort kam
        
    def sendData(self, data_array):
        if not data_array or len(data_array) != 4:
            print("Error: Data array must have exactly 4 elements!")
            return

        data_to_send = data_array.copy()
        data_len = len(data_to_send)
        data_to_send.insert(0, data_len)  # Länge an den Anfang setzen
        data_string = ",".join(map(str, data_to_send)) + "\n"

        self.serial.write(data_string.encode())
        self.serial.flush()
        print(f"Sent: {data_string.strip()}")

        time.sleep(0.1)  # Wartezeit, um nicht zu oft zu senden


    def close(self):
        self.serial.close()

class SerialInterfaceWebsocket:
    def __init__(self, serial_interface, ip, port, update_callback):
        self.serial_interface = serial_interface
        self.ip = ip
        self.port = port
        self.update_callback = update_callback  # Callback zum Aktualisieren des dataArray

    async def handle_client(self, websocket, path):
        async for message in websocket:
            try:
                numbers = list(map(int, message.split(",")))
                if len(numbers) == 4 and all(0 <= num <= 255 for num in numbers):
                    print("getnumbers:", numbers)
                else:
                    print("Fehlerhafte Daten empfangen:", message)
            except ValueError:
                print("Ungültiges Format:", message)

    async def start_server(self):
        server = await websockets.serve(self.handle_client, self.ip, self.port)
        print(f"WebSocket-Server läuft auf ws://{self.ip}:{self.port}")
        await server.wait_closed()
