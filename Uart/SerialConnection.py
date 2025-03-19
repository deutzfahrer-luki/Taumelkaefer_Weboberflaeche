import RPi.GPIO as GPIO
import serial
import time
import logging

class IOs:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        
    def setState(self, state):
        GPIO.output(self.pin, GPIO.HIGH if state else GPIO.LOW)
        
    def impuls(self, impulseDuration = 0.4, normalstate = 1):
        GPIO.output(self.pin, GPIO.LOW if normalstate else GPIO.HIGH)
        time.sleep(impulseDuration)
        GPIO.output(self.pin, GPIO.HIGH if normalstate else GPIO.LOW) 
        time.sleep(impulseDuration*2)

class SerialConnection:
    def __init__(self, port, rstPin, baudrate=115200, timeout=2):
        self.port = port
        self.timeout = timeout  # Timeout für die Antwort vom ESP32
        self.rstPin = rstPin
        self.reset = IOs(self.rstPin)
        self.reset.setState(True)
        time.sleep(1)
        try:
            self.serial = serial.Serial(port=port, baudrate=baudrate, timeout=1)
            logging.info(f"Serielle Verbindung geöffnet: {port} bei {baudrate} Baud.")
        except Exception as e:
            logging.error(f"Fehler beim Öffnen der seriellen Verbindung: {e}")
            self.reset.impuls()
            raise e

    def sendData(self, dataArray):
        dataArray = [len(dataArray)] + dataArray
        try:
            self.dataString = ', '.join(str(data) for data in dataArray)
            self.serial.write(f"{self.dataString}\n".encode())
            logging.info(f"Gesendet an {self.port} (ESP32): {self.dataString}")
            response = self.waitForResponse()

            if response == self.dataString:
                logging.info(f"Antwort vom ESP32 erhalten: {response}")
                return True
            else:
                logging.error("Timeout: Keine Antwort vom ESP32 erhalten.")
                self.reset.impuls()
                return False
        except Exception as e:
            logging.error(f"Fehler beim Senden der Daten: {e}")
            return False

    def waitForResponse(self):
        start_time = time.time()
        while time.time() - start_time < self.timeout:
            if self.serial.in_waiting > 0:
                response = self.serial.readline().decode('utf-8').strip()
                return response
            time.sleep(0.1)
        return None

    def closeConnection(self):
        if self.serial.is_open:
            self.serial.close()
            self.reset.setState(False)
            logging.info("Serielle Verbindung geschlossen.")
        else:
            logging.info("Serielle Verbindung war bereits geschlossen.")
