fetch('settings/config.json')
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP-Fehler! Status: ${response.status}`);
    }
    return response.json();
  })
  .then(config => {
    const ip = config.ip;
    const port = config.port_Stream;
    const streamUrl = `http://${ip}:${port}/stream.mjpg`;

    console.log('Stream URL:', streamUrl); // Debugging-Log

    document.getElementById('mjpegStream').src = streamUrl;
  })
  .catch(error => console.error('Fehler beim Laden der JSON:', error));
