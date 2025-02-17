function sendData() {
    const inputData = document.getElementById('dataInput').value;
    const dataArray = inputData.split(',').map(num => parseInt(num.trim(), 10)).filter(num => !isNaN(num));

    if (dataArray.length === 0) {
        document.getElementById('response').innerText = "Bitte gültige Zahlen eingeben!";
        return;
    }

    // TCP-Verbindung zum Raspberry Pi (mit WebSocket)
    const socket = new WebSocket('ws://192.168.178.38:5001');  // Überprüfe die IP-Adresse hier

    socket.onopen = () => {
        console.log("Verbindung hergestellt");
        document.getElementById('response').innerText = "Verbindung hergestellt. Sende Daten...";

        // Daten im richtigen Format senden (CSV als Text)
        socket.send(dataArray.join(','));
        console.log("Daten gesendet:", dataArray.join(','));
    };

    socket.onmessage = (event) => {
        // Antwort vom Server empfangen und anzeigen
        console.log("Antwort vom Server:", event.data);
        document.getElementById('response').innerText = `Antwort vom ESP32: ${event.data}`;
        socket.close();
    };

    socket.onerror = (error) => {
        console.log("WebSocket Fehler:", error);
        document.getElementById('response').innerText = "Fehler bei der Verbindung.";
    };

    socket.onclose = () => {
        console.log("Verbindung geschlossen");
    };
}
