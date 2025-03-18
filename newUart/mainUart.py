import asyncio
import websockets
from SerialConnection import *
from UartWebserver import *
# from GPIOs.gpio import IOs

print("TestSkript Uart connection and Uart Websoket")

data = [255, 255, 255, 255]
olddata = data

se = SerialConnection(port='/dev/ttyS0', baudrate=115200)
web = UartWebsocket()

async def websocket_server():
    """Startet den WebSocket-Server."""
    async with websockets.serve(web.handler, "192.168.1.114", 8765):
        await asyncio.Future()

async def monitor_data():
    """Überprüft kontinuierlich, ob sich die Daten geändert haben."""
    global data, olddata
    while True:
        data = web.getData()
        if data != olddata:
            print(data)
            olddata = data
            se.sendData(olddata)
        await asyncio.sleep(0.1)

async def main():
    """Startet sowohl den WebSocket-Server als auch die Datenüberwachung."""
    await asyncio.gather(websocket_server(), monitor_data())

if __name__ == "__main__":
    asyncio.run(main())
