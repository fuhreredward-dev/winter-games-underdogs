"""
Simple backend to save schedule data from admin.html

This runs a local server that:
1. Serves the admin interface
2. Saves schedule data when the admin makes changes

Usage:
    python scripts/admin_server.py
    
Then visit: http://localhost:8000/admin.html
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import base64
import json
import os
from pathlib import Path
from datetime import datetime


ADMIN_USER = os.environ.get("ADMIN_USER", "admin")
ADMIN_PASS = os.environ.get("ADMIN_PASS", "changeme")


class AdminHandler(SimpleHTTPRequestHandler):
    def _is_protected_path(self, path: str) -> bool:
        return path in (
            "/admin.html",
            "/api/save-schedule",
            "/data/schedule-data.json",
        )

    def _unauthorized(self):
        self.send_response(401)
        self.send_header("WWW-Authenticate", 'Basic realm="Admin"')
        self.end_headers()

    def _check_auth(self) -> bool:
        auth = self.headers.get("Authorization", "")
        if not auth.startswith("Basic "):
            return False
        try:
            decoded = base64.b64decode(auth.split(" ", 1)[1]).decode("utf-8")
            user, password = decoded.split(":", 1)
            return user == ADMIN_USER and password == ADMIN_PASS
        except Exception:
            return False

    def do_GET(self):
        if self._is_protected_path(self.path) and not self._check_auth():
            self._unauthorized()
            return
        super().do_GET()

    def do_POST(self):
        """Handle POST requests to save schedule data."""
        if self._is_protected_path(self.path) and not self._check_auth():
            self._unauthorized()
            return
        if self.path == '/api/save-schedule':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            
            try:
                data = json.loads(body)
                
                # Save to schedule-data.json
                output_file = Path('data/schedule-data.json')
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                # Send success response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {
                    'success': True,
                    'message': f'Schedule saved at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
                }
                self.wfile.write(json.dumps(response).encode('utf-8'))
                
                print(f"✓ Schedule saved at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {
                    'success': False,
                    'message': str(e)
                }
                self.wfile.write(json.dumps(response).encode('utf-8'))
                print(f"❌ Error saving schedule: {e}")
        else:
            super().do_POST()

    def end_headers(self):
        """Add CORS headers."""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()


def main():
    port = 8000
    server = HTTPServer(('localhost', port), AdminHandler)
    
    print(f"""
╔═══════════════════════════════════════════════════════════════╗
║            🏔️  Olympic Admin Server Started                   ║
╚═══════════════════════════════════════════════════════════════╝

Admin Interface: http://localhost:{port}/admin.html
Schedule Data:  http://localhost:{port}/data/schedule-data.json

Auth: Basic (ADMIN_USER/ADMIN_PASS env vars)
Default: admin / changeme

Press Ctrl+C to stop the server.
""")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n✓ Server stopped")


if __name__ == '__main__':
    main()
