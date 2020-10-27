import sys
import socket
from server.ping import *
from server.ConnectionClosedException import ConnectionClosedException


class Server:

    def __init__(self, address):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(address)
        self.sock.listen(BACKLOG)

    def run(self):
        while True:
            # when EOF reached, finish
            line = sys.stdin.readline()
            if not line:
                break

            conn, addr = self.sock.accept()
            if not conn:
                break

            try:
                ping_type = receive(conn, PING_BYTES)
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
