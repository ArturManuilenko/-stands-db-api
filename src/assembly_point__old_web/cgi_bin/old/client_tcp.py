import os
import socket
import client
import ast


class TCPClient(client.Client):
    def __init__(self, *args, **wargs):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        self.client.connect(("127.0.0.1", os.environ['BACKEND_PORT']))
        return super().__init__(*args, **wargs)

    def __del__(self):
        self.client.close()

    def make_command(self):
        self.client.send(str(self.request).encode() + b'\n')
        ans_str = b''
        while True:
            rx = self.client.recv(256*1024*1024).split(b'\n')
            ans_str = ans_str + rx[0]
            if len(rx) == 2:
                break

        self.answer = ast.literal_eval(ans_str.decode())
