fetch('config.json')
    .then(response => response.json())
    .then(config => {
        const streamUrl = `http://${config.ip}:${config.port_Stream}/stream.mjpg`;
        document.getElementById('mjpegStream').src = streamUrl;
    })
    .catch(error => console.error('Fehler beim Laden der JSON:', error));