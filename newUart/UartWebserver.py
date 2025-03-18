import asyncio
import websockets

class UartWebsocket:
    def __init__(self):
        self.numbers = [0, 0, 0, 0]

    async def handler(self, websocket, path):
        async for message in websocket:
            try:
                self.numbers = list(map(int, message.split(",")))
                if len(self.numbers) == 4 and all(0 <= num <= 255 for num in self.numbers):
                    print("getnumbers:", self.numbers)
                else:
                    print("Fehlerhafte Daten empfangen:", message)
            except ValueError:
                print("Ungültiges Format:", message)
                
    def getData(self):
        return self.numbers            



