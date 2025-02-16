// Funktion, um die JSON-Datei zu laden
fetch('settings/config.json')
.then(response => response.json())  // JSON antwort einlesen
.then(data => {
    // IP-Adresse aus der JSON-Datei extrahieren
    const ip = data.ip;

    // Die URL für den MJPEG Stream zusammenstellen
    const streamUrl = `http://${ip}:7123/stream.mjpg`;

    // Das img-Tag mit der URL des Streams aktualisieren
    document.getElementById('mjpegStream').src = streamUrl;
})
.catch(error => {
    console.error('Fehler beim Laden der JSON-Datei:', error);
});