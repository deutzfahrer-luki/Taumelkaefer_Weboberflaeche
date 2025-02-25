from settings.configLoad import ConfigLoader
from Stream.streamingServer import Stream
from UART.uartWebserverOld import SerialWebSocketServer
import asyncio


# --------------------  load settings  -------------------- #
config = ConfigLoader("settings/config.json")
IP = config.get("ip")
PORT_INTERFACE = config.get("port_Interface")
PORT_STREAM = config.get("port_Stream")
PORT_UART = config.get("port_UART")


# --------------------  stream  -------------------- #
stream = Stream(IP, PORT_STREAM)


# --------------------  UART interface  -------------------- #
SERIAL_PORT = "/dev/ttyS0"
uart = SerialWebSocketServer(host=IP, baudrate=115200, port=SERIAL_PORT, serial_port=SERIAL_PORT)


# --------------------  main  -------------------- #
if __name__ == "__main__":
    print(f"IP: {IP}, Webpage Port: {PORT_INTERFACE}, Stream: {PORT_STREAM}, UART Port: {PORT_UART}")
    # stream.start()
    uart.send_serial_data("10")
    # asyncio.run(uart.start_server())
