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
        
    def sendData(self, data_array):
        if not data_array:
            print("Error: Data array is empty!")
            return
        else:
            self.dataArray = data_array.copy()
        
        self.len = len(data_array)
        
        self.dataArray.insert(0, self.len)
        
        data_string = ",".join(map(str, self.dataArray)) + "\n"
        
        self.serial.write(data_string.encode())
        self.serial.flush()
        print(f"Sent: {data_string.strip()}")

    def close(self):
        self.serial.close()

def serialTest(len):
    for i in range(len):
        Raspi.sendData([i,i,i,i])
        time.sleep(0.3)


Raspi = SerialInterface(SerialPort=SERIAL_PORT, Baudrate=BAUDRATE)


try:
    # Raspi.sendData([-255, 255, 255, 255])
    serialTest(255)

except serial.SerialException as e:
    print(f"Fehler: {e}")

finally:
    Raspi.close()

# from uart import *
# import asyncio

# SERIAL_PORT = "/dev/ttyS0"
# uart = SerialWebSocketServer(host="172.16.15.68", baudrate=115200, port=7123, serial_port=SERIAL_PORT)

# if __name__ == "__main__":
#     uart.send_serial_data("10")
