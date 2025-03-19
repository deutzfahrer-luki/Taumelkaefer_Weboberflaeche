import io
import logging
import socketserver
import asyncio
from http import server
from threading import Condition
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput

PAGE = """
<html>
<head><title>Picamera2 MJPEG Streaming</title></head>
<body>
<h1>Picamera2 MJPEG Streaming</h1>
<img src="stream.mjpg" width="640" height="480" />
</body>
</html>
"""

class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()
        logging.info("StreamingOutput initialized.")
    
    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        logging.info(f"Received GET request: {self.path}")
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(f'Removed streaming client {self.client_address}: {e}')
        else:
            self.send_error(404)
            self.end_headers()
            logging.warning(f"404 Not Found: {self.path}")

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

class Stream:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.picam2 = None
        self.server = None

    async def start(self):
        global output

        logging.info("Starting Picamera2...")
        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_video_configuration(main={"size": (640, 480)}))
        output = StreamingOutput()
        self.picam2.start_recording(JpegEncoder(), FileOutput(output))

        address = (self.ip, int(self.port))
        self.server = StreamingServer(address, StreamingHandler)

        logging.info(f"Streaming Server läuft auf http://{self.ip}:{self.port}")
        
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self.server.serve_forever)
    
    async def stop(self):
        logging.info("Stopping Picamera2...")
        if self.picam2:
            self.picam2.stop_recording()
        if self.server:
            self.server.shutdown()
        logging.info("Stream stopped.")