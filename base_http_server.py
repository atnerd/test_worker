import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from remote_storage import remote_storage
from worker import init_workers, storage_lock, task_queue


class RequestHandler(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def do_GET(self):
        if not self.path == "/results":
            self.send_response(404)
            self.wfile.write(b"Invalid address")
            return
        self._set_response()
        with storage_lock:
            self.wfile.write(json.dumps(remote_storage).encode("utf-8"))

    def do_POST(self):
        if not self.path == "/submit":
            self.send_response(404)
            self.wfile.write(b"Invalid address")
            return
        content_length = int(self.headers["Content-Length"])
        post_data = json.loads(self.rfile.read(content_length))
        numbers = post_data.get("numbers")
        if not numbers or not all(isinstance(n, int) and 1 <= n <= 99 for n in numbers):
            self.send_response(400)
            self.wfile.write(b"Invalid input")
        else:
            task_queue.put(numbers)
            self._set_response()
            self.wfile.write(b"Data received")


def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    init_workers()
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting httpd on port {port}...")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
