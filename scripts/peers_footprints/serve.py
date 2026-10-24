import http.server, socketserver, os, sys, urllib.request, mimetypes
ROOT = sys.argv[1]; PORT = int(sys.argv[2])
class H(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        p = path.split('?')[0]
        if p.startswith('/curated/'):
            return os.path.join(ROOT, p[len('/curated/'):].lstrip('/'))
        return os.path.join(ROOT, '__none__')
    def do_GET(self):
        p = self.path
        if p.startswith('/static/'):
            fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static_dl', os.path.basename(p.split('?')[0]))
            if os.path.exists(fn):
                body = open(fn, 'rb').read(); self.send_response(200)
                self.send_header('Content-Type', 'application/javascript'); self.send_header('Content-Length', str(len(body))); self.end_headers(); self.wfile.write(body)
            else:
                self.send_error(404)
            return
        path = self.translate_path(p)
        if os.path.isdir(path):
            idx = os.path.join(path, 'index.html')
            if os.path.exists(idx): self.path = p.rstrip('/') + '/index.html'
        return super().do_GET()
    def log_message(self, *a): pass
socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(('127.0.0.1', PORT), H) as s: s.serve_forever()
