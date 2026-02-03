"""
Start local server and open SkyMarshal Dashboard
Just double-click this file or run: py start_dashboard.py
"""
import http.server
import socketserver
import webbrowser
import os

PORT = 8080

os.chdir(os.path.dirname(os.path.abspath(__file__)))

print(f"Starting SkyMarshal Dashboard server on http://localhost:{PORT}")
print("Press Ctrl+C to stop the server")

# Open browser
webbrowser.open(f'http://localhost:{PORT}/skymarshal.html')

# Start server
with socketserver.TCPServer(("", PORT), http.server.SimpleHTTPRequestHandler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
