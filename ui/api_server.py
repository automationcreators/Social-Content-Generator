#!/usr/bin/env python3
"""
RSS Idea Selector API Server
Serves the UI and handles idea selection + script generation
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
from pathlib import Path
import sys
from datetime import datetime
import subprocess

class APIHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.base_dir = Path(__file__).parent.parent
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if self.path == '/':
            self.path = '/ui/rss_idea_selector.html'
            return super().do_GET()

        elif self.path == '/api/ideas':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            # Load RSS ideas from JSON
            rss_file = self.base_dir / 'scouts' / 'rss_ideas_database.json'
            with open(rss_file, 'r') as f:
                data = json.load(f)

            self.wfile.write(json.dumps(data).encode())
            return

        else:
            return super().do_GET()

    def do_POST(self):
        if self.path == '/api/generate-scripts':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            selected_ideas = data.get('selected_ideas', [])

            # Save selected ideas to a file for the generator to use
            selected_file = self.base_dir / 'scouts' / 'selected_ideas.json'
            with open(selected_file, 'w') as f:
                json.dump({
                    'selected_date': datetime.now().isoformat(),
                    'ideas': selected_ideas
                }, f, indent=2)

            # Run the script generator
            try:
                result = subprocess.run([
                    'python3',
                    str(self.base_dir / 'generators' / 'generate_from_selected.py')
                ], capture_output=True, text=True, timeout=300)

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()

                response = {
                    'success': True,
                    'scripts_created': len(selected_ideas),
                    'output_location': '/active/Social-Content-Generator/pillar_scripts/',
                    'stdout': result.stdout,
                    'stderr': result.stderr
                }

                self.wfile.write(json.dumps(response).encode())

            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()

                self.wfile.write(json.dumps({
                    'success': False,
                    'error': str(e)
                }).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def run(port=8888):
    server_address = ('', port)
    httpd = HTTPServer(server_address, APIHandler)
    print(f"""
    ========================================
    🚀 RSS Idea Selector UI
    ========================================

    📊 Access the UI at:
    http://localhost:{port}

    🔧 API Endpoints:
    GET  /api/ideas - List all RSS ideas
    POST /api/generate-scripts - Generate scripts from selected ideas

    Press Ctrl+C to stop
    ========================================
    """)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n✅ Server stopped")
        sys.exit(0)

if __name__ == '__main__':
    run()
