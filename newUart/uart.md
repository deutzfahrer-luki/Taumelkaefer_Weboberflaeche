# Nutzung des Codes

## 1. Starten des Python-Servers

Der Python-Server besteht aus drei Hauptdateien:

- **main.py**: Startet den WebSocket-Server und überwacht empfangene Daten.
- **UartWebserver.py**: Behandelt WebSocket-Nachrichten.
- **SerialConnection.py**: Kommuniziert über UART mit einem ESP32 oder einem anderen Gerät.

### Starten des Servers:
```sh
python3 main.py
```

## 2. WebSocket-Client (HTML + JavaScript)

Ein einfacher WebSocket-Client kann über die Datei `index.html` genutzt werden.

### Aufbau:
- Ein Eingabefeld für vier Zahlen (0-255, durch Kommas getrennt).
- Ein Button zum Senden der Daten an den WebSocket-Server.
- JavaScript für die WebSocket-Kommunikation.

### Nutzung:
1. Öffne die `index.html`-Datei im Browser.
2. Gib vier Zahlen (z. B. `10,20,30,40`) in das Eingabefeld ein.
3. Klicke auf "Daten senden", um die Werte an den Server zu senden.

## 3. Methoden und ihre Nutzung

### **UartWebsocket** (UartWebserver.py)
- `handler(websocket, path)`: Empfängt und verarbeitet WebSocket-Nachrichten.
- `getData()`: Gibt die zuletzt empfangenen Zahlen zurück.

### **SerialConnection** (SerialConnection.py)
- `sendData(dataArray)`: Sendet ein Array über die serielle Schnittstelle.
- `closeConnection()`: Schließt die serielle Verbindung.

### **mainUart.py**
- `websocket_server()`: Startet den WebSocket-Server.
- `monitor_data()`: Prüft auf neue Daten und sendet sie per UART.
- `main()`: Startet WebSocket und Datenüberwachung gleichzeitig zum Testen.
