#!/usr/bin/env python3
import http.server
import socketserver
import os
from pathlib import Path
from urllib.parse import urlparse

PORT = 8000
DIRECTORY = "html"

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, directory=None, **kwargs):
        super().__init__(*args, directory=directory, **kwargs)

    def do_GET(self):
        # Redirect / to /index.html
        if self.path == '/':
            self.path = '/index.html'
        return super().do_GET()

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        return super().end_headers()

# Create html directory if it doesn't exist
os.makedirs(DIRECTORY, exist_ok=True)

# Change to the html directory so server serves from there
os.chdir(DIRECTORY)

handler = lambda *args: MyHTTPRequestHandler(*args, directory=".")

with socketserver.TCPServer(("", PORT), handler) as httpd:
    print(f"Server running at http://localhost:{PORT}")
    print(f"Serving files from: {os.path.abspath('.')}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
