import asyncio
import websockets
import logging

class LogWebSocketServer:
    def __init__(self, host, port, logfile):
        self.host = host
        self.port = port
        self.logfile = logfile
        self.logger = logging.getLogger(__name__)

    async def log_reader(self, websocket, path):
        """Liest die Log-Datei und sendet jede Zeile an den WebSocket-Client."""
        try:
            with open(self.logfile, 'r') as log_file:
                while True:
                    line = log_file.readline()
                    if line:
                        await websocket.send(line)
                    else:
                        await asyncio.sleep(1)
        except websockets.exceptions.ConnectionClosed as e:
            self.logger.error(f"WebSocket-Verbindung Log geschlossen: {e}")
        finally:
            self.logger.info("WebSocket-Verbindung Log wurde beendet.")

    async def start(self):
        """Startet den WebSocket-Server."""
        async with websockets.serve(self.log_reader, self.host, self.port):
            self.logger.info(f"WebSocket-Server Log läuft auf ws://{self.host}:{self.port}")
            await asyncio.Future()



