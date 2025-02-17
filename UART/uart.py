import serial
import socket
import threading
import time
import websockets
import asyncio

# ---------- Konfiguration ----------
HOST = '0.0.0.0'  # Der Server hört auf allen Schnittstellen
PORT = 5001        # Der Port, den der WebSocket-Server verwenden soll

ESPserial = serial.Serial('/dev/ttyS0', 9600, timeout=1)  # UART0, 115200 Baud

sendData = [140, 150, 200, 255]
sendBytes = bytes(sendData)

time.sleep(2)

def send_Serial_Data(data):
    print("Func SendData")
    ESPserial.write(data)
    print(f"Gesendet: {list(data)}")
    ESPserial.flush()
    time.sleep(0.5)

def get_Serial_Data():
    start_time = time.time()
    while ESPserial.in_waiting < 4:
        if time.time() - start_time > 2:  # Timeout nach 2 sec
            print("Keine Antwort erhalten")
            return None  # Rückgabe von None, falls kein gültiges Paket empfangen wurde

    if ESPserial.in_waiting >= 4:
        recvData = ESPserial.read(4)
        print(f"Empfangene Antwort: {list(recvData)}")
        return recvData
    else:
        print("Fehlerhaft")
        return None

async def handle_client(websocket, path):
    try:
        print("Neue WebSocket-Verbindung von:", websocket.remote_address)

        # Empfange Daten vom WebSocket-Client
        data = await websocket.recv()
        print(f"Empfangene Daten vom Client: {data}")  # Ausgabe der empfangenen Daten im Terminal

        # Daten in Bytes umwandeln und an den ESP32 senden
        numbers = list(map(int, data.split(',')))
        sendBytes = bytes(numbers)
        send_Serial_Data(sendBytes)

        # Antwort vom ESP32 empfangen
        response = get_Serial_Data()
        if response is not None:
            # Sende die Antwort an den WebSocket-Client zurück
            await websocket.send(response)
        else:
            await websocket.send("ERROR: Keine Antwort vom ESP32")

    except Exception as e:
        print(f"Fehler: {e}")
        await websocket.send(f"ERROR: {str(e)}")

    finally:
        print("Verbindung geschlossen")
        await websocket.close()

async def start_server():
    # Starte den WebSocket-Server auf dem Raspberry Pi
    server = await websockets.serve(handle_client, HOST, PORT)
    print(f"✅ WebSocket-Server läuft auf ws://{HOST}:{PORT}")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(start_server())
