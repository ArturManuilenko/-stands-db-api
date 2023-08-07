import client_tcp

cl = client_tcp.TCPClient()
cl.service_command('exit')
print(cl.answer)
input('closed')
