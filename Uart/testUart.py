from UartWebsocketHandler import *
import logging
import asyncio

print("TestSkript Uart connection and Uart WebSocket")

with open('server_log.log', 'w'): 
    pass

logging.basicConfig(filename='server_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info("TestSkript Uart connection und Uart WebSocket gestartet")

UH = UartWebsocketHandler(ip="192.168.1.114", port=8765, rstPin=18)

async def main():
    """Startet den WebSocket-Server und wartet auf KeyboardInterrupt"""
    try:
        await UH.main()
    except asyncio.CancelledError:
        logging.info("Async-Task wurde abgebrochen.")
    except KeyboardInterrupt:
        logging.info("KeyboardInterrupt erkannt, fahre System herunter...")
    finally:
        await UH.shutdown()
        logging.info("Shutdown abgeschlossen.")
        print("\nServer gestoppt.")

if __name__ == "__main__":
    asyncio.run(main())

