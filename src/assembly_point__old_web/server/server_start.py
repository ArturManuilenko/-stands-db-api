import server_handler

import time

with open("log", "a") as f:
    f.write("{} started \n".format(time.asctime()))

try:
        server = server_handler.Server()
        server.run()
        with open("log", "a") as f:
            f.write("{} exited \n".format(time.asctime()))
except Exception as e:
    with open("log", "a") as f:
        f.write("{} error: {}\n".format(time.asctime(), str(e)))


