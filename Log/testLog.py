from log import LogWebSocketServer
import logging
import asyncio

with open('Log/server_log.log', 'w'): 
    pass

logging.basicConfig(filename='Log/server_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info("TestSkript Uart connection und Uart WebSocket gestartet")

if __name__ == "__main__":
    server = LogWebSocketServer("192.168.1.114", 5678, 'Log/server_log.log')
    asyncio.run(server.start())
