import asyncio
import websockets
from SerialConnection import *
from UartWebserver import *

print("Hallo World")

data = [255, 255, 255, 255]
olddata = data

se = SerialConnection(port='/dev/ttyS0', baudrate=115200)
web = UartWebsocket()

async def websocket_server():
    """Startet den WebSocket-Server."""
    async with websockets.serve(web.handler, "172.16.15.68", 8765):
        await asyncio.Future()  # Blockiert für immer (ersetzt run_forever())

async def monitor_data():
    """Überprüft kontinuierlich, ob sich die Daten geändert haben."""
    global data, olddata
    while True:
        data = web.getData()  # Falls es eine Methode ist, nutze web.getData()
        if data != olddata:
            print(data)
            olddata = data
            se.sendData(olddata)
        await asyncio.sleep(0.1)  # Verhindert übermäßige CPU-Auslastung

async def main():
    """Startet sowohl den WebSocket-Server als auch die Datenüberwachung."""
    await asyncio.gather(websocket_server(), monitor_data())

if __name__ == "__main__":
    asyncio.run(main())
