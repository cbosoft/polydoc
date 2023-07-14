from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class WebRequestHandler(BaseHTTPRequestHandler):
    """simple web server, replies 'ok!' to anything POST'd to it."""

    def do_POST(self):
        '''POST request handler method. Recieves an object sect via post (by the [send_data](multi/site/index.js|Function:send_data) function)'''
        length = int(self.headers.getheader('content-length'))
        incoming = self.rfile.read(length)
        incoming = json.loads(incoming)
        print(incoming)

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        reply = json.dumps(dict(
            message='ok!',
        ))
        self.wfile.write(reply.encode("utf-8"))


def run_server():
    """
    start http server and server forever.

    Uses [WebRequestHandler] for handling responses.
    """
    server = HTTPServer('127.0.0.1', WebRequestHandler)
    server.server_forever()
