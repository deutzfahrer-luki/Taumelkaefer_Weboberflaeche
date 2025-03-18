import serial
import time

class SerialConnection:
    def __init__(self, port, baudrate=115200):
        try:
            self.serial = serial.Serial(port=port, baudrate=baudrate, timeout=1)
            print(f"Serielle Verbindung geöffnet: {port} bei {baudrate} Baud.")
        except Exception as e:
            print(f"Fehler beim Öffnen der seriellen Verbindung: {e}")

    def sendData(self, dataArray):
        dataArray = [len(dataArray)] + dataArray
        try:
            dataString = ', '.join(str(data) for data in dataArray)
            # for number in dataArray:
            self.serial.write(f"{dataString}\n".encode())
            time.sleep(0.5)
            print("gesendet:", dataString)
        except Exception as e:
            print(f"Fehler beim Senden der Daten: {e}")

    def closeConnection(self):
        if self.serial.is_open:
            self.serial.close()
            print("Serielle Verbindung geschlossen.")
        else:
            print("Serielle Verbindung war bereits geschlossen.")



