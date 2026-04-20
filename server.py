from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import unquote
class R(BaseHTTPRequestHandler):
    def do_POST(self):
        target = unquote(self.path[1:])
        self.send_response(302)
        self.send_header("Location", target)
        self.end_headers()
    do_GET = do_POST
HTTPServer(("0.0.0.0", 8080), R).serve_forever()
