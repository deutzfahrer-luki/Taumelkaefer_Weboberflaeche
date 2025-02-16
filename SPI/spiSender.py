import spidev
import time
import os

spi = spidev.SpiDev()
spi.open(0, 0)  
spi.max_speed_hz = 500000  

def send_spi_data():
    while True:
        if os.path.exists("/tmp/spi_data.txt"):
            with open("/tmp/spi_data.txt", "r") as f:
                data = f.read().strip()
                if data:
                    print(f"Sende: {data}")
                    spi.xfer2([ord(c) for c in data])
                    open("/tmp/spi_data.txt", "w").close()  # Datei leeren
        time.sleep(1)

send_spi_data()
