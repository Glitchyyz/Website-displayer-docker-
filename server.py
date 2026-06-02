#!/usr/bin/env python3
import http.server
import socketserver
import os
import ssl
import json
import urllib.request
from urllib.parse import urlparse

PORT = 8000 
DIRECTORY = "html"

# --- TRUENAS PROXY CONFIGURATION ---
TRUENAS_IP = "192.168.2.149"
# Pulls directly from the container's environment variables
TRUENAS_API_KEY = os.environ.get("TRUENAS_API_KEY")

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, directory=None, **kwargs):
        super().__init__(*args, directory=directory, **kwargs)

    def do_GET(self):
        clean_path = urlparse(self.path).path.rstrip('/')
        if clean_path == '/api/truenas-proxy':
            self.handle_truenas_proxy()
            return

        if self.path == '/':
            self.path = '/index.html'
        return super().do_GET()

    def handle_truenas_proxy(self):
        # Error handling if you forgot to pass the environment variable
        if not TRUENAS_API_KEY:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "TRUENAS_API_KEY environment variable is not set!"}).encode('utf-8'))
            return

        url = f"https://{TRUENAS_IP}/api/v2.0/system/info"
        req = urllib.request.Request(url)
        req.add_header("Authorization", f"Bearer {TRUENAS_API_KEY}")
        req.add_header("Content-Type", "application/json")
        
        ssl_context = ssl._create_unverified_context()
        
        try:
            with urllib.request.urlopen(req, context=ssl_context) as response:
                data = response.read()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*') 
                self.end_headers()
                self.wfile.write(data)
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            err_msg = json.dumps({"error": str(e)}).encode('utf-8')
            self.wfile.write(err_msg)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.send_header('Access-Control-Allow-Origin', '*')
        return super().end_headers()

os.makedirs(DIRECTORY, exist_ok=True)
os.chdir(DIRECTORY)

socketserver.TCPServer.allow_reuse_address = True
handler = lambda *args: MyHTTPRequestHandler(*args, directory=".")

with socketserver.TCPServer(("", PORT), handler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass