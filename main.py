import asyncio
import logging
from settings.configLoad import ConfigLoader
from Stream.streamingServer import Stream
from Uart.UartWebsocketHandler import UartWebsocketHandler
from Log.log import LogWebSocketServer

# --------------------Log -------------------- #
with open('Log/server_log.log', 'w'): 
    pass

logging.basicConfig(filename='Log/server_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info("TestSkript Uart connection und Uart WebSocket gestartet")
logserver = LogWebSocketServer("192.168.1.114", 5678, 'Log/server_log.log')

# -------------------- Einstellungen laden -------------------- #
config = ConfigLoader("settings/config.json")
IP = config.get("ip")
PORT_INTERFACE = config.get("port_Interface")
PORT_STREAM = config.get("port_Stream")
PORT_UART = config.get("port_UART")
RST_PIN = config.get("esp32_GPIO_RST")

# -------------------- Stream -------------------- #
stream = Stream(IP, PORT_STREAM)

# -------------------- UART-Interface -------------------- #
UartHandler = UartWebsocketHandler(ip=IP, port=PORT_UART, rstPin=RST_PIN)

async def main():
    """Startet den Stream und das WebSocket-Interface asynchron."""
    try:
        logging.info(f"Starte Server mit IP: {IP}, WebSocket Port: {PORT_INTERFACE}, Stream Port: {PORT_STREAM}, UART Port: {PORT_UART}")

        # Asynchrone Tasks für Stream und UART starten
        stream_task = asyncio.create_task(stream.start())
        uart_task = asyncio.create_task(UartHandler.start())
        log_task = asyncio.create_task(logserver.start())

        await asyncio.gather(stream_task, uart_task)

    except KeyboardInterrupt:
        logging.info("KeyboardInterrupt erkannt, fahre System herunter...")
    finally:
        await stream.stop()
        await UartHandler.shutdown()
        logging.info("Shutdown abgeschlossen.")
        print("\nServer gestoppt.")

if __name__ == "__main__":
    asyncio.run(main())
