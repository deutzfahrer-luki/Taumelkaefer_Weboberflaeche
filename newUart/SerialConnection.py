import serial
import time
import logging

class SerialConnection:
    def __init__(self, port, baudrate=115200, timeout=2):
        self.port = port
        self.timeout = timeout  # Timeout für die Antwort vom ESP32
        try:
            self.serial = serial.Serial(port=port, baudrate=baudrate, timeout=1)
            logging.info(f"Serielle Verbindung geöffnet: {port} bei {baudrate} Baud.")
        except Exception as e:
            logging.error(f"Fehler beim Öffnen der seriellen Verbindung: {e}")
            raise e

    def sendData(self, dataArray):
        dataArray = [len(dataArray)] + dataArray
        try:
            dataString = ', '.join(str(data) for data in dataArray)
            self.serial.write(f"{dataString}\n".encode())
            logging.info(f"Gesendet an {self.port} (ESP32): {dataString}")
            
            # Warten auf Antwort vom ESP32
            response = self.waitForResponse()

            if response:
                logging.info(f"Antwort vom ESP32 erhalten: {response}")
            else:
                logging.error("Timeout: Keine Antwort vom ESP32 erhalten.")
        except Exception as e:
            logging.error(f"Fehler beim Senden der Daten: {e}")

    def waitForResponse(self):
        start_time = time.time()
        while time.time() - start_time < self.timeout:
            if self.serial.in_waiting > 0:
                response = self.serial.readline().decode('utf-8').strip()
                return response
            time.sleep(0.1)  # Kurze Pause, um nicht die CPU zu blockieren
        return None  # Falls keine Antwort innerhalb des Timeouts kommt

    def closeConnection(self):
        if self.serial.is_open:
            self.serial.close()
            logging.info("Serielle Verbindung geschlossen.")
        else:
            logging.info("Serielle Verbindung war bereits geschlossen.")
