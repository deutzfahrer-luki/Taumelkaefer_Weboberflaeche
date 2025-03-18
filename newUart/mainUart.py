import asyncio
import websockets
from SerialConnection import *
from UartWebserver import *
import logging
# from GPIOs.gpio import IOs

print("TestSkript Uart connection and Uart Websoket")

# Logdatei zu Beginn leeren (überschreiben)
with open('server_log.log', 'w'): 
    pass  # Einfach nur die Datei im 'w' Modus öffnen, um sie zu leeren

logging.basicConfig(filename='server_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info("TestSkript Uart connection und Uart WebSocket gestartet")

data = [255, 255, 255, 255]
olddata = data

se = SerialConnection(port='/dev/ttyS0', baudrate=115200)
web = UartWebsocket()

async def websocket_server():
    """Startet den WebSocket-Server und protokolliert die Aktivität."""
    logging.info("Starte WebSocket-Server...")
    try:
        async with websockets.serve(web.handler, "192.168.1.114", 8765):
            logging.info("WebSocket-Server läuft auf ws://192.168.1.114:8765")
            await asyncio.Future()  # Hält den Server am Laufen
    except Exception as e:
        logging.error(f"Fehler beim Starten des WebSocket-Servers: {e}")

async def monitor_data():
    """Überprüft kontinuierlich, ob sich die Daten geändert haben und protokolliert Änderungen."""
    global data, olddata
    while True:
        data = web.getData()
        if data != olddata:
            logging.info(f"Neue Daten empfangen: {data}")
            olddata = data
            se.sendData(olddata)
        await asyncio.sleep(0.1)

async def main():
    """Startet sowohl den WebSocket-Server als auch die Datenüberwachung und protokolliert den Start."""
    logging.info("Starte WebSocket-Server und Datenüberwachung...")
    await asyncio.gather(websocket_server(), monitor_data())

if __name__ == "__main__":
    asyncio.run(main())
