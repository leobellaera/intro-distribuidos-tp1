import socket
from socket import gaierror
from datetime import datetime as dt
from common.utils import send, receive, get_random_string, \
    ConnectionClosedException
from common.constants import ACK_MSG, PACKAGE_LEN, COUNT_LEN, ACK_LEN, \
    TIMEOUT_SECONDS, DISCARDED_PCK_RTT, DEST_ADDR_LEN, DIRECT_PING, ERR_MSG


class DirectPing:
    def __init__(self, conn):
        self.conn = conn
        send(conn, ACK_MSG)

    def run(self):
        while True:
            try:
                receive(self.conn, PACKAGE_LEN)
            except ConnectionClosedException:
                break  # Error is expected as client closes connection wh done
            send(self.conn, ACK_MSG)


class ReversePing:
    def __init__(self, conn):
        send(conn, ACK_MSG)
        self.count = int(receive(conn, COUNT_LEN))
        self.conn = conn

    def run(self):
        for i in range(self.count):
            initial_dt = dt.now()
            send(self.conn, get_random_string(PACKAGE_LEN))
            receive(self.conn, ACK_LEN)
            final_dt = dt.now()

            delta = final_dt - initial_dt
            if delta.seconds >= TIMEOUT_SECONDS:
                send(self.conn, str(DISCARDED_PCK_RTT))
                continue

            delta = round((delta.seconds + delta.microseconds / 1000000.0) *
                          1000, 1)
            delta = "{:07.1f}".format(delta)
            send(self.conn, delta)
        self.conn.close()


class ProxyPing:
    def __init__(self, conn):
        self.client_conn = conn

        self.count = int(receive(conn, COUNT_LEN))

        addr_len = int(receive(conn, DEST_ADDR_LEN))
        dest_addr_split = receive(conn, addr_len).split(':')
        dest_addr = (dest_addr_split[0], int(dest_addr_split[1]))

        # create socket and connect to proxy
        self.proxy_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # handshaking with proxy sv to begin direct ping
        try:
            self.proxy_conn.connect(dest_addr)
            send(self.proxy_conn, DIRECT_PING)
            receive(self.proxy_conn, ACK_LEN)
        except (gaierror, ConnectionRefusedError, ConnectionClosedException) \
                as e:
            send(self.client_conn, ERR_MSG)
            raise ConnectionClosedException(str(e))

        send(self.client_conn, ACK_MSG)

    def run(self):
        for i in range(self.count):

            initial_dt = dt.now()

            try:
                send(self.proxy_conn, get_random_string(PACKAGE_LEN))
                receive(self.proxy_conn, ACK_LEN)
            except ConnectionClosedException as e:
                send(self.client_conn, ERR_MSG)
                raise ConnectionClosedException(str(e))

            final_dt = dt.now()
            send(self.client_conn, ACK_MSG)

            delta = final_dt - initial_dt
            if delta.seconds >= TIMEOUT_SECONDS:
                send(self.client_conn, str(DISCARDED_PCK_RTT))
                continue

            delta = round((delta.seconds + delta.microseconds / 1000000.0) *
                          1000, 1)
            delta = "{:07.1f}".format(delta)
            send(self.client_conn, delta)
