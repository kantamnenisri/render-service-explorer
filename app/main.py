import http.server
import socketserver
import json
import os
import urllib.request
import urllib.error
import sys

PORT = 8000
RENDER_API_URL = "https://api.render.com/v1"

# Absolute path setup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")

# Improved .env loading
API_KEY = None
if os.path.exists(ENV_PATH):
    try:
        with open(ENV_PATH, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "RENDER_API_KEY" in line:
                    parts = line.split("=", 1)
                    if len(parts) == 2:
                        API_KEY = parts[1].strip().strip('"').strip("'")
        print(f"Loaded API Key: {'Present' if API_KEY else 'Missing'}")
    except Exception as e:
        print(f"Error reading .env: {e}")

class RenderHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Log all requests
        print(f"Request: {self.path}")

        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open(os.path.join(BASE_DIR, 'static', 'index.html'), 'rb') as f:
                self.wfile.write(f.read())
            return
        
        elif self.path == '/api/services':
            try:
                services = self.fetch_render_services()
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(services).encode())
            except Exception as e:
                print(f"Server Error in API: {e}")
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
            return
            
        else:
            # For local dev, manually serve files from static folder
            if self.path.startswith('/static/'):
                return super().do_GET()
            
            # Default fallthrough
            return super().do_GET()

    def fetch_render_services(self):
        # Return mock data if key is placeholder or missing
        if not API_KEY or API_KEY == "xxx" or len(API_KEY) < 5:
            print("Mode: Demo/Mock Data")
            return [
                {"id": "1", "name": "Demo Web Service", "type": "web_service", "status": "live", "url": "https://demo.onrender.com", "repo": "https://github.com/demo", "updated_at": "2024-03-10T12:00:00Z"},
                {"id": "2", "name": "Demo Static Site", "type": "static_site", "status": "live", "url": "https://static.onrender.com", "repo": "https://github.com/static", "updated_at": "2024-03-09T10:00:00Z"},
                {"id": "3", "name": "Weekly Report", "type": "cron_job", "status": "suspended", "updated_at": "2024-03-01T08:00:00Z"},
            ]

        print(f"Mode: Real API Request to Render")
        req = urllib.request.Request(f"{RENDER_API_URL}/services?limit=100")
        req.add_header("Authorization", f"Bearer {API_KEY}")
        req.add_header("Accept", "application/json")

        try:
            with urllib.request.urlopen(req, timeout=15) as response:
                res_data = response.read().decode()
                raw_data = json.loads(res_data)
                unified = []
                for item in raw_data:
                    svc = item.get("service", {})
                    details = svc.get("serviceDetails", {})
                    url = details.get("url") if svc.get("type") in ["static_site", "web_service"] else None
                    
                    unified.append({
                        "id": svc.get("id"),
                        "name": svc.get("name"),
                        "type": svc.get("type"),
                        "status": svc.get("status"),
                        "url": url,
                        "repo": svc.get("repo"),
                        "updated_at": svc.get("updatedAt") or "2024-01-01T00:00:00Z"
                    })
                print(f"Success: Fetched {len(unified)} services")
                return unified
        except urllib.error.HTTPError as e:
            error_msg = e.read().decode()
            print(f"API HTTP Error: {e.code} - {error_msg}")
            # Instead of returning empty list, raise to show error on UI
            raise Exception(f"Render API returned {e.code}: {error_msg}")
        except Exception as e:
            print(f"Connection Error: {e}")
            raise Exception(f"Failed to connect to Render: {str(e)}")

if __name__ == "__main__":
    os.chdir(BASE_DIR)
    socketserver.TCPServer.allow_reuse_address = True
    print(f"Starting server on http://localhost:{PORT}")
    with socketserver.TCPServer(("0.0.0.0", PORT), RenderHandler) as httpd:
        httpd.serve_forever()
