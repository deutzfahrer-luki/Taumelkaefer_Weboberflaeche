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
        """Setzt den Pin auf HIGH oder LOW."""
        GPIO.output(self.pin, GPIO.HIGH if state else GPIO.LOW)
        
    def impuls(self, impulseDuration=0.4, normalstate=1):
        """Sendet einen Impuls an den Pin und kehrt dann zurück."""
        GPIO.output(self.pin, GPIO.LOW if normalstate else GPIO.HIGH)
        time.sleep(impulseDuration)
        GPIO.output(self.pin, GPIO.HIGH if normalstate else GPIO.LOW) 
        time.sleep(impulseDuration * 2)

    def cleanup(self):
        """Freigabe der GPIOs, um Fehler zu vermeiden."""
        GPIO.cleanup()  # Setzt alle Pins zurück und gibt sie frei

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
        """Sendet Daten an das ESP32 über die serielle Verbindung und erwartet eine Antwort."""
        dataArray = [len(dataArray)] + dataArray
        try:
            self.dataString = ', '.join(str(data) for data in dataArray)
            self.serial.write(f"{self.dataString}\n".encode())
            logging.info(f"Gesendet an {self.port} (ESP32): {self.dataString}")
            response = self.waitForResponse()
            # logging.info(f"Antwort vom ESP32 erhalten (raw): {repr(response)}")
            # logging.info(f"Gesendete Daten (raw): {repr(self.dataString)}")

            if response and response.strip() == self.dataString.strip():
                logging.info(f"Antwort vom ESP32 erhalten: {response}")
                return True
            else:
                logging.error(f"Timeout: Keine Antwort vom ESP32 erhalten oder Antwort stimmt nicht überein. Antwort: {response} und gesendete Daten: {self.dataString}")
                self.reset.impuls()
                return False
        except Exception as e:
            logging.error(f"Fehler beim Senden der Daten: {e}")
            return False

    def waitForResponse(self):
        """Wartet auf eine Antwort vom ESP32 innerhalb des angegebenen Timeouts."""
        start_time = time.time()
        while time.time() - start_time < self.timeout:
            if self.serial.in_waiting > 0:
                response = self.serial.readline().decode('utf-8').strip()
                return response
            time.sleep(0.1)
        logging.warning("Timeout beim Warten auf Antwort.")
        return None

    def closeConnection(self):
        """Schließt die serielle Verbindung."""
        if self.serial.is_open:
            self.serial.close()
            self.reset.setState(False)
            logging.info("Serielle Verbindung geschlossen.")
        else:
            logging.info("Serielle Verbindung war bereits geschlossen.")
    
    @staticmethod  
    def checkArray(array1, array2):
        """Vergleicht zwei Arrays und gibt zurück, ob sie identisch sind."""
        if len(array1) != len(array2):
            return False
        for i in range(len(array1)):
            if array1[i] != array2[i]:
                return False
        return True
