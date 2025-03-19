import asyncio
import websockets
import logging

class UartWebsocket:
    def __init__(self):
        self.numbers = [0, 0, 0, 0]

    async def handler(self, websocket, path):
        async for message in websocket:
            try:
                self.numbers = list(map(int, message.split(",")))
                if len(self.numbers) == 4 and all(0 <= num <= 255 for num in self.numbers):
                    logging.info(f"Empfangene Zahlen vom WebSocket: {self.numbers}")
                else:
                    logging.warning(f"Fehlerhafte Daten empfangen: {message}")
            except ValueError:
                logging.warning(f"Ungültiges Format empfangen: {message}")
                
    def getData(self):
        return self.numbers
