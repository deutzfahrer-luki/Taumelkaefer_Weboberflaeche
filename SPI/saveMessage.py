#!/usr/bin/env python3

import cgi
import spidev
import time

# CGI-Header für HTML-Antwort
print("Content-Type: text/html\n")
print("<html><body><h2>Nachricht gespeichert & gesendet!</h2></body></html>")

# Nachricht aus Formular holen
form = cgi.FieldStorage()
message = form.getvalue("message", "")

# Nachricht in Datei speichern
if message:
    with open("/tmp/spi_data.txt", "w") as f:
        f.write(message)

# SPI einrichten
spi = spidev.SpiDev()
spi.open(0, 0)  # SPI0, Chip Select 0
spi.max_speed_hz = 500000  # Geschwindigkeit

# Nachricht in Bytes umwandeln & senden
spi.xfer2([ord(c) for c in message])
time.sleep(0.1)

# SPI schließen
spi.close()
