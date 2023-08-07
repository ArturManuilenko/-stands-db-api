import os
import socket
import select
import ast
import command_handler

items = {}

class Server:
    def __init__(self):
        self.allow_process = True

    def run(self):
        print('------------------ server started -------------------')
        self.allow_process = True

        server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('', int(os.environ['BACKEND_PORT'])))
        server.listen(20)
    

        read_list = [server]

        command_handler.start()
        print('------------------ server listen -------------------')

        while self.allow_process:
            readable, writable, errored = select.select(read_list, [], read_list, 10)
            for s in readable:
                if s == server:
                    client, address = server.accept()
                    if address[0] == '127.0.0.1':
                        read_list.append(client)
                        items[client.fileno()] = ['']
                    else:
                        client.close()
                else:
                    try:
                        rx = s.recv(64*1024*1024)
                    except: rx = b''
                    if len(rx) == 0:
                        s.close()
                        read_list.remove(s)
                    else:
                        self.process_request(s, rx.decode())

        for sock in read_list:
            sock.close()
        print('------------------ server stopped -------------------')

    def process_request(self, s, data):
        cmds = data.split('\n')
        cmds[0] = items[s.fileno()][0] + cmds[0]

        for cmd in cmds:
            if len(cmd):
                res = self.make_command(cmd) + '\n'
                s.send(res.encode())

        items[s.fileno()][0] = cmds[-1]

    def make_command(self, cmd):
        print('req: {}'.format(cmd))
        cmd = ast.literal_eval(cmd)
        res = str(command_handler.process(cmd))
        self.allow_process = command_handler.run_status
        print('ans: {}'.format(res[:1024]))
        return res
    
if __name__ == "__main__":
   
    try:
        server = Server()
        server.run()
    except Exception as e:
        print(e)

