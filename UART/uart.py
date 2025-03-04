import serial
import time

SERIAL_PORT = "/dev/serial0"  # Oder "/dev/ttyS0"
BAUDRATE = 115200

class SerialInterface:
    def __init__(self, SerialPort, Baudrate):
        print("init UART (maybe Running)")
        self.serialPort = SerialPort
        self.bautrate = Baudrate
        self.serial = serial.Serial(self.serialPort, self.bautrate, timeout=1)
        print(f"start connection on {self.serialPort} with {self.bautrate}")
        time.sleep(2)
        
        
    def initial(self, ip, timeout=10, delay=1):
        start_time = time.time()
        self.ipencoded = ip.encode()

        while time.time() - start_time < timeout:
            # IP erneut senden, solange keine Antwort kommt
            self.serial.write(self.ipencoded)  
            self.serial.flush()
            print(f"Initial UART Send to Start the ESP32 on {ip}")

            # Warte auf Antwort
            wait_start = time.time()
            while time.time() - wait_start < 0.5:
                if self.serial.in_waiting:  # Prüft, ob Daten verfügbar sind
                    received_ip = self.serial.read(len(self.ipencoded))
                    if received_ip == self.ipencoded:
                        print(f"ESP32 antwortet mit der gleichen IP: {ip}")
                        return ip  # Gibt die IP zurück, wenn sie übereinstimmt

                time.sleep(delay)

        print("Timeout erreicht. Keine Antwort vom ESP32 erhalten.")
        return None  # Falls keine Antwort kam
        
    def sendData(self, data_array):
        if not data_array or len(data_array) != 4:
            print("Error: Data array must have exactly 4 elements!")
            return

        data_to_send = data_array.copy()
        data_len = len(data_to_send)
        data_to_send.insert(0, data_len)  # Länge an den Anfang setzen
        data_string = ",".join(map(str, data_to_send)) + "\n"

        self.serial.write(data_string.encode())
        self.serial.flush()
        print(f"Sent: {data_string.strip()}")

        time.sleep(0.1)  # Wartezeit, um nicht zu oft zu senden


    def close(self):
        self.serial.close()
            

def serialTest(len):
    for i in range(len):
        Raspi.sendData([i,i,i,i])
        time.sleep(0.3)

# Test code
# Raspi = SerialInterface(SerialPort=SERIAL_PORT, Baudrate=BAUDRATE)
# Raspi.initial('172.16.15.68')

# try:
#     # Raspi.sendData([-255, 255, 255, 255])
#     serialTest(255)

# except serial.SerialException as e:
#     print(f"Fehler: {e}")

# finally:
#     Raspi.close()


