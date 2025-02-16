# todos
-   Pyhton server automatisch starten

# Kamera Dienste
## stream Dienst installieren
sudo apt update
sudo apt install gstreamer1.0-tools gstreamer1.0-plugins-good gstreamer1.0-plugins-bad

## Dienst starten (muss daweil noch laufen bleiben)
libcamera-vid -t 0 --framerate 30 --width 1280 --height 720 --codec h264 --bitrate 2000000 | \
gst-launch-1.0 -v fdsrc ! h264parse ! avdec_h264 ! videoconvert ! jpegenc ! rtpjpegpay ! udpsink host=127.0.0.1 port=5000


# SPI
## HTML Teil
    <h2>SPI Nachricht senden</h2>
    <form action="/cgi-bin/save_message.py" method="post">
        <input type="text" name="message" placeholder="Nachricht eingeben">
        <input type="submit" value="Senden">
    </form>
## CGI-Skript zum Speichern der Nachricht
sudo a2enmod cgi
sudo systemctl restart apache2

## Skritp in python schreiben 
ausführbar machen: sudo chmod +x /var/www/html/SPI/saveMessage.py


<Directory "/home/pi/cgi-bin">
    AllowOverride None
    Options +ExecCGI -MultiViews +SymLinksIfOwnerMatch
    Require all granted
    AddHandler cgi-script .py
</Directory>