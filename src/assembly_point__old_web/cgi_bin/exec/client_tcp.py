import os
import socket
from src.assembly_point__old_web.cgi_bin.exec.client import Client
import ast


class TCPClient(Client):
    def __init__(self, *args, **kwargs) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        self.client.connect(("", int(os.environ['BACKEND_PORT'])))
        return super().__init__(*args, **kwargs)

    def __del__(self) -> None:
        self.client.close()

    def make_command(self) -> None:
        self.client.send(str(self.request).encode() + b'\n')
        ans_str = b''
        while True:
            rx = self.client.recv(256 * 1024 * 1024).split(b'\n')
            ans_str = ans_str + rx[0]
            if len(rx) == 2:
                break

        self.answer = ast.literal_eval(ans_str.decode())
