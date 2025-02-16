import serial
import time

ESPserial = serial.Serial('/dev/ttyS0', 9600, timeout=1)  # UART0, 115200 Baud

time.sleep(2)

send_data = [101,150,200,255]
send_bytes = bytes(send_data)

DATA_IN = 4
DATA_OUT = len(send_data)


while True:
	# send Data to ESP32
	ESPserial.write(send_bytes)
	print(f"Gesendet (nicht empfangen): {list(send_data)}")
	ESPserial.flush()
	time.sleep(0.5)

	# resice Data from ESP32
	start_time = time.time()
	while ESPserial.in_waiting < 4:
		if time.time() - start_time > 2: 	#timeout nach 2 sec
			print("Keine Antowrt erhalten")
			break

	if ESPserial.in_waiting >= 4:
		recv_data = ESPserial.read(4)
		print(f"Empfangene Antwort: {list(recv_data)}")
	else:
		print("Fehlerhaft")

	# ready with this shit
	time.sleep(2)
