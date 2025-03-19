import asyncio
import websockets
import logging

class UartWebsocket:
    def __init__(self):
        self.numbers = [0, 0, 0, 0]

    async def handler(self, websocket, path):
        async for message in websocket:
            try:
                received_values = list(map(int, message.split(",")))
                if len(received_values) == 4 and all(0 <= num <= 255 for num in received_values):
                    self.numbers = received_values
                    # logging.info(f"Empfangene gültige Zahlen vom WebSocket: {self.numbers}")
                else:
                    logging.warning(f"Fehlerhafte Daten empfangen (ungültige Anzahl oder Werte): {message}")
                    self.numbers = [0, 0, 0, 0]
            except ValueError:
                logging.warning(f"Ungültiges Format empfangen: {message}")
                self.numbers = [0, 0, 0, 0]

                
    def getData(self):
        return self.numbers
