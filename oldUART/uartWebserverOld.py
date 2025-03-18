import serial
import time
import asyncio
import websockets

class SerialWebSocketServer:
    def __init__(self, serial_port='/dev/ttyS0', baudrate=9600, host='0.0.0.0', port=5001):
        self.serial_port = serial_port
        self.baudrate = baudrate
        self.host = host
        self.port = port
        self.esp_serial = serial.Serial(self.serial_port, self.baudrate, timeout=1)
        time.sleep(2)  # Wartezeit für die Initialisierung

    def send_serial_data(self, data):
        print("Sende Daten an ESP32")
        self.esp_serial.write(data)
        print(f"Gesendet: {list(data)}")
        self.esp_serial.flush()
        time.sleep(0.5)

    def get_serial_data(self):
        start_time = time.time()
        while self.esp_serial.in_waiting < 4:
            if time.time() - start_time > 2:  # Timeout nach 2 Sekunden
                print("Keine Antwort erhalten")
                return None

        if self.esp_serial.in_waiting >= 4:
            recv_data = self.esp_serial.read(4)
            print(f"Empfangene Antwort: {list(recv_data)}")
            return recv_data
        else:
            print("Fehlerhaftes Paket erhalten")
            return None

    async def handle_client(self, websocket, path):
        try:
            print("Neue WebSocket-Verbindung von:", websocket.remote_address)
            data = await websocket.recv()
            print(f"Empfangene Daten vom Client: {data}")

            # Eingehende Daten in Bytes konvertieren
            numbers = list(map(int, data.split(',')))
            send_bytes = bytes(numbers)
            self.send_serial_data(send_bytes)

            # Antwort vom ESP32 empfangen
            response = self.get_serial_data()
            if response is not None:
                await websocket.send(response)
            else:
                await websocket.send("ERROR: Keine Antwort vom ESP32")

        except Exception as e:
            print(f"Fehler: {e}")
            await websocket.send(f"ERROR: {str(e)}")

        finally:
            print("Verbindung geschlossen")
            await websocket.close()

    async def start_server(self):
        server = await websockets.serve(self.handle_client, self.host, self.port)
        print(f"WebSocket-Server läuft auf ws://{self.host}:{self.port}")
        await server.wait_closed()
