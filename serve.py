#!/usr/bin/env python3
"""
Local development server for previewing the built site.
"""

import http.server
import socketserver
import os
from pathlib import Path

PORT = 8000
DIST_DIR = Path(__file__).parent / "dist"


def serve():
    if not DIST_DIR.exists():
        print(f"Error: {DIST_DIR} does not exist. Run 'uv run build.py' first.")
        return

    os.chdir(DIST_DIR)

    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        print("Press Ctrl+C to stop")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down...")


if __name__ == "__main__":
    serve()
