import RPi.GPIO as GPIO
import time

class ESP32Resetter:
    def __init__(self, reset_pin=17):
        """
        Initialisiert den Resetter für den ESP32.

        :param reset_pin: Der GPIO-Pin des Raspberry Pi, der mit dem EN-Pin des ESP32 verbunden ist (Standard: GPIO 17)
        """
        self.reset_pin = reset_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.reset_pin, GPIO.OUT)

    def reset(self):
        print("ESP32 wird zurückgesetzt...")
        GPIO.output(self.reset_pin, GPIO.LOW)  # EN-Pin auf LOW setzen (Reset)
        time.sleep(0.1)  # Warten, damit der Reset durchführt werden kann
        GPIO.output(self.reset_pin, GPIO.HIGH)  # EN-Pin auf HIGH setzen (normaler Betrieb)
        print("ESP32 zurückgesetzt.")

    def cleanup(self):
        """
        Setzt den GPIO-Pin auf den Ausgangszustand zurück.
        """
        GPIO.cleanup()
        
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
                    

# Beispielverwendung:
# if __name__ == "__main__":
#     esp32_resetter = ESP32Resetter(reset_pin=17)  # Erstelle eine Instanz der Klasse
#     try:
#         esp32_resetter.reset()  # ESP32 zurücksetzen
#     except KeyboardInterrupt:
#         print("Program abgebrochen.")
#     finally:
#         esp32_resetter.cleanup()  # GPIO sauber freigeben
