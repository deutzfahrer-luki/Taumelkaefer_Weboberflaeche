from settings.configLoad import ConfigLoader

config = ConfigLoader("settings/config.json")
IP = config.get("ip")
PORT_INTERFACE = config.get("port_Interface")
PORT_STREAM = config.get("port_Stream")
PORT_UART = config.get("port_UART")


if __name__ == "__main__":  
    print(f"IP: {IP}, Webpage Port: {PORT_INTERFACE}, Stream: {PORT_STREAM}, UART Port: {PORT_UART}")
    
    
#     config = ConfigLoader()
#     print(config.get("ip"))
