import serial
import time
import asyncio
import websockets

class SerialInterface:
    def __init__(self, SerialPort, Baudrate):
        print("init UART (maybe Running)")
        self.serialPort = SerialPort
        self.bautrate = Baudrate
        self.serial = serial.Serial(self.serialPort, self.bautrate, timeout=1)
        print(f"start connection on {self.serialPort} with {self.bautrate}")
        time.sleep(2)
        
        
    def initial(self, ip, timeout=10, delay=1):
        start_time = time.time()
        self.ipencoded = ip.encode()

        while time.time() - start_time < timeout:
            # IP erneut senden, solange keine Antwort kommt
            self.serial.write(self.ipencoded)  
            self.serial.flush()
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
        try:
            print(f"Neue WebSocket-Verbindung von: {websocket.remote_address}")
            
            async for message in websocket:
                print(f"Empfangene Daten vom Client: {message}")

                try:
                    # Erwartet werden vier kommagetrennte Zahlen
                    numbers = list(map(int, message.split(",")))
                    if len(numbers) != 4:
                        await websocket.send("ERROR: Es müssen genau 4 Werte gesendet werden!")
                        continue

                    # Hier wird das Callback aufgerufen (Beispiel: Rückgabe des Arrays)
                    updated_array = self.update_callback(*numbers)

                    # Sende das Array (als JSON) zurück an den Client:
                    await websocket.send(json.dumps(updated_array))
                    
                except ValueError:
                    await websocket.send("ERROR: Ungültiges Format! Erwartet: '100,150,200,250'")
        except Exception as e:
            print(f"Fehler: {e}")
            await websocket.send(f"ERROR: {str(e)}")
        finally:
            print("WebSocket-Verbindung geschlossen")
            await websocket.close()

    async def start_server(self):
        server = await websockets.serve(self.handle_client, self.ip, self.port)
        print(f"WebSocket-Server läuft auf ws://{self.ip}:{self.port}")
        await server.wait_closed()
