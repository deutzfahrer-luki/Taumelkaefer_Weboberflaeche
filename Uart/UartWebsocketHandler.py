import asyncio
import websockets
from .SerialConnection import *
from .UartWebserver import *
import logging

class UartWebsocketHandler:
    def __init__(self, ip, port, rstPin):
        self.ip = ip
        self.port = port
        self.rstPin = rstPin
        self.se = SerialConnection(port='/dev/ttyS0', baudrate=115200, rstPin=self.rstPin)
        self.web = UartWebsocket()
        self.data = [0, 0, 0, 0]
        self.olddata = self.data
        self.server = None  # Initialisiere server als None
        
    async def websocket_server(self):
        """Startet den WebSocket-Server."""
        logging.info("Starte WebSocket-Server...")
        self.server = await websockets.serve(self.web.handler, self.ip, self.port)
        logging.info(f"WebSocket-Server läuft auf ws://{self.ip}:{self.port}")
        await asyncio.Future()  # Hält den Server am Laufen


    async def monitor_data(self):
        """Überprüft kontinuierlich, ob sich die Daten geändert haben."""
        while True:
            self.resultuion = False
            self.data = self.web.getData()
            if self.data != self.olddata:
                logging.info(f"Neue Daten empfangen: {self.data}")
                self.olddata = self.data
                while self.resultuion == False:
                    self.resultuion = self.se.sendData(self.olddata)
            await asyncio.sleep(0.1)

    async def start(self):
        """Startet WebSocket-Server und Datenüberwachung."""
        logging.info("Starte WebSocket-Server und Datenüberwachung...")
        await asyncio.gather(self.websocket_server(), self.monitor_data())
        
    async def shutdown(self):
        """Beendet den WebSocket-Server und die Datenüberwachung sicher."""
        logging.info("Fahre System herunter...")
        
        if self.server:  # Prüft, ob self.server existiert
            self.server.close()
            await self.server.wait_closed()
            logging.info("WebSocket-Server gestoppt.")

        self.se.closeConnection()
        logging.info("UART Connection geschlossen und ESP ausgeschaltet über Enable")
