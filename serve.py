#!/usr/bin/env python3
"""
Local development server with live reload.

Watches for changes in posts/ and templates/, rebuilds, and triggers browser refresh.
"""

import http.server
import json
import os
import socketserver
import threading
import time
from pathlib import Path

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Import build function
from build import build, POSTS_DIR, TEMPLATES_DIR, OUTPUT_DIR

PORT = 8000
ROOT = Path(__file__).parent

# Track last build time for live reload
last_build_time = time.time()
build_lock = threading.Lock()


class RebuildHandler(FileSystemEventHandler):
    """Rebuild site when source files change."""

    def on_any_event(self, event):
        global last_build_time

        # Ignore directory events and hidden files
        if event.is_directory:
            return
        if '/.' in event.src_path or event.src_path.startswith('.'):
            return

        # Debounce rapid changes
        with build_lock:
            current_time = time.time()
            if current_time - last_build_time < 0.5:
                return

            print(f"\nChange detected: {event.src_path}")
            try:
                build()
                last_build_time = time.time()
            except Exception as e:
                print(f"Build error: {e}")


class LiveReloadHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP handler that injects live reload script into HTML pages."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(OUTPUT_DIR), **kwargs)

    def do_GET(self):
        # Serve build timestamp for live reload polling
        if self.path == '/__reload__':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            self.wfile.write(json.dumps({'time': last_build_time}).encode())
            return

        super().do_GET()

    def end_headers(self):
        # Add no-cache headers for development
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

    def send_head(self):
        """Inject live reload script into HTML responses."""
        path = self.translate_path(self.path)

        # Handle directory index
        if os.path.isdir(path):
            path = os.path.join(path, 'index.html')

        if path.endswith('.html') and os.path.exists(path):
            with open(path, 'rb') as f:
                content = f.read()

            # Inject live reload script before </body>
            reload_script = b'''
<script>
(function() {
  let lastTime = 0;
  async function checkReload() {
    try {
      const res = await fetch('/__reload__');
      const data = await res.json();
      if (lastTime && data.time > lastTime) {
        location.reload();
      }
      lastTime = data.time;
    } catch (e) {}
    setTimeout(checkReload, 500);
  }
  checkReload();
})();
</script>
</body>'''
            content = content.replace(b'</body>', reload_script)

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()

            # Return a BytesIO-like object
            import io
            return io.BytesIO(content)

        return super().send_head()

    def copyfile(self, source, outputfile):
        """Copy file, handling our injected content."""
        import shutil
        shutil.copyfileobj(source, outputfile)


def serve():
    if not OUTPUT_DIR.exists():
        print("Building site first...")
        build()

    # Set up file watcher
    observer = Observer()
    handler = RebuildHandler()

    # Watch posts and templates directories
    if POSTS_DIR.exists():
        observer.schedule(handler, str(POSTS_DIR), recursive=True)
    if TEMPLATES_DIR.exists():
        observer.schedule(handler, str(TEMPLATES_DIR), recursive=True)

    observer.start()

    # Start HTTP server
    with socketserver.TCPServer(("", PORT), LiveReloadHandler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        print(f"Watching {POSTS_DIR} and {TEMPLATES_DIR} for changes")
        print("Press Ctrl+C to stop\n")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down...")
            observer.stop()

    observer.join()


if __name__ == "__main__":
    serve()
