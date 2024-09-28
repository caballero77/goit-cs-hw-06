import datetime
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import os
import pathlib
import logging
import mimetypes
import socket


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


http_port = int(os.getenv("HTTP_PORT", 3000))
socket_port = int(os.getenv("SOCKET_PORT", 5000))


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == "/":
            self.send_html_file("front/index.html")
        elif pr_url.path == "/message.html":
            self.send_html_file("front/message.html")
        else:
            if pathlib.Path().joinpath("front").joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file("front/error.html", 404)

    def do_POST(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == "/message":
            data = self.rfile.read(int(self.headers["Content-Length"]))
            data_parse = urllib.parse.unquote_plus(data.decode())
            data_dict = {
                key: value
                for key, value in [el.split("=") for el in data_parse.split("&")]
            }
            
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect(("localhost", socket_port))

                data_dict["date"] = str(datetime.datetime.now())
                client.send(json.dumps(data_dict).encode("utf-8"))

            self.send_html_file("front/message.html")

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with open(filename, "rb") as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", "text/plain")
        self.end_headers()
        with open(f"./front/{self.path}", "rb") as file:
            self.wfile.write(file.read())


def run_http_server():
    server_address = ("", http_port)
    http = HTTPServer(server_address, HttpHandler)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()
