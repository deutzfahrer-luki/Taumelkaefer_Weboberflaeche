import serial
import time

# Initialisiere die serielle Verbindung (mit den GPIO Pins 10 für TX und 8 für RX)
# Überprüfe, dass '/dev/ttyS0' korrekt ist, oder versuche '/dev/ttyAMA0' je nach Setup
ser = serial.Serial('/dev/ttyS0', 115200, timeout=1)

# Warte eine Sekunde, um sicherzustellen, dass die serielle Verbindung funktioniert
time.sleep(2)

# Die 5 Zahlen, die gesendet werden sollen
numbers = [23, 56, 12, 99, 8]

try:
    while True:
        for number in numbers:
            # Sende jede Zahl gefolgt von einem Newline-Zeichen
            ser.write(f"{number}\n".encode())  
            print(f"Gesendet: {number}")  # Debug-Ausgabe, um die gesendeten Zahlen zu sehen
            time.sleep(0.5)  # Kurze Pause zwischen den Sendungen

        time.sleep(1)  # Warte eine Sekunde, bevor die Zahlen erneut gesendet werden
        print("Wiederhole das Senden der Zahlen...")

except KeyboardInterrupt:
    print("Senden abgebrochen durch Benutzer.")

finally:
    # Schließe die serielle Verbindung, wenn das Programm beendet wird
    ser.close()
    print("Serielle Verbindung geschlossen.")
