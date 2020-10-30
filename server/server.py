import sys
import socket

from common.constants import PROXY_PING, REVERSE_PING, BACKLOG, \
    PING_TYPE_LEN, DIRECT_PING
from common.exceptions import ConnectionClosedException
from common.utils import receive
from server.ping import DirectPing, ReversePing, ProxyPing


class Server:

    def __init__(self, address):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(address)
        self.sock.listen(BACKLOG)

    def run(self):
        while True:
            conn, addr = self.sock.accept()
            if not conn:
                print("Server socket closed", file=sys.stderr)
                break

            try:
                ping_type = receive(conn, PING_TYPE_LEN)
                if ping_type == DIRECT_PING:
                    print("Running Direct Ping")
                    DirectPing(conn).run()
                elif ping_type == REVERSE_PING:
                    print("Running Reverse Ping")
                    ReversePing(conn).run()
                elif ping_type == PROXY_PING:
                    print("Running Proxy Ping")
                    ProxyPing(conn).run()
                print("DONE!")
            except ConnectionClosedException as e:
                print(f"ERROR: {str(e)}")
            finally:
                conn.close()

        self.sock.close()
