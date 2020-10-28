from common.utils import *
from common.constants import *
from common.exceptions import ConnectionClosedException
from server.ping import *


class Server:

    def __init__(self, address):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(address)
        self.sock.listen(BACKLOG)

    def run(self):
        while True:
            conn, addr = self.sock.accept()
            if not conn:  #todo print error msg
                break

            try:
                ping_type = receive(conn, PING_TYPE_LEN)
                if ping_type == DIRECT_PING:
                    DirectPing(conn).run()
                elif ping_type == REVERSE_PING:
                    ReversePing(conn).run()
                elif ping_type == PROXY_PING:
                    ProxyPing(conn).run()

            except ConnectionClosedException as e:
                conn.close()
                print(str(e))

        self.sock.close()
