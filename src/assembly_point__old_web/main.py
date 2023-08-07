import os
from http.server import HTTPServer, CGIHTTPRequestHandler
if __name__ == "__main__":
    server_address = ("", int(os.environ['APPLICATION_PORT']))
    handler = CGIHTTPRequestHandler
    handler.cgi_directories = ['/cgi_bin', '/src', '/old']
    httpd = HTTPServer(server_address, handler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.socket.close()
