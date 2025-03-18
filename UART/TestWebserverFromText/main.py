import asyncio
import websockets

async def handler(websocket, path):
    async for message in websocket:
        try:
            # Konvertiere die empfangenen Daten in eine Liste von Zahlen
            numbers = list(map(int, message.split(",")))
            
            # Überprüfe, ob genau 4 Zahlen empfangen wurden und alle 8-Bit sind
            if len(numbers) == 4 and all(0 <= num <= 255 for num in numbers):
                print("Empfangene Zahlen:", numbers)
            else:
                print("Fehlerhafte Daten empfangen:", message)
        except ValueError:
            print("Ungültiges Format:", message)

# Starte den WebSocket-Server
print("hallo World")
start_server = websockets.serve(handler, "172.16.15.68", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
