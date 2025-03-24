import RPi.GPIO as GPIO
import time
import asyncio
import websockets

# GPIO-Setup
SERVO_PIN = 18  # Ändere dies entsprechend deiner Verkabelung
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

# PWM initialisieren
pwm = GPIO.PWM(SERVO_PIN, 50)  # 50 Hz PWM für Servo
pwm.start(7.5)  # Mittelstellung (90 Grad)

def set_angle(angle):
    duty_cycle = 2.5 + (angle / 18)  # Umrechnung von Grad in Duty Cycle
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.5)  # Kurze Wartezeit zur Stabilisierung

async def websocket_handler(websocket, path):
    async for message in websocket:
        if message.isdigit():
            angle = int(message)
            if 0 <= angle <= 180:
                set_angle(angle)
                await websocket.send(f"Servo auf {angle} Grad eingestellt")
            else:
                await websocket.send("Bitte einen Wert zwischen 0 und 180 eingeben.")
        elif message.lower() == "lidar":
            await websocket.send("LIDAR-Modus gestartet")
            start_angle, end_angle, delay = 0, 180, 0.1
            while True:
                for angle in range(start_angle, end_angle + 1, 5):
                    set_angle(angle)
                    await asyncio.sleep(delay)
                for angle in range(end_angle, start_angle - 1, -5):
                    set_angle(angle)
                    await asyncio.sleep(delay)
        elif message.lower() == "exit":
            await websocket.send("Server wird gestoppt")
            return
        else:
            await websocket.send("Ungültige Eingabe")

start_server = websockets.serve(websocket_handler, "0.0.0.0", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

pwm.stop()
GPIO.cleanup()

# HTML-Datei zur Steuerung (Speichern als servo_control.html)
html_code = """
<!DOCTYPE html>
<html>
<head>
    <title>Servo Steuerung</title>
    <script>
        var ws = new WebSocket("ws://" + window.location.hostname + ":8765");

        function sendAngle() {
            var angle = document.getElementById("angleInput").value;
            ws.send(angle);
        }

        function startLidar() {
            ws.send("lidar");
        }
    </script>
</head>
<body>
    <h1>Servo Steuerung</h1>
    <input type="number" id="angleInput" min="0" max="180" placeholder="Winkel (0-180)">
    <button onclick="sendAngle()">Setze Winkel</button>
    <button onclick="startLidar()">LIDAR Modus</button>
</body>
</html>
"""

with open("servo_control.html", "w") as file:
    file.write(html_code)
