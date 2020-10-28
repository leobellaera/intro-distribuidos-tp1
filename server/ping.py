from datetime import datetime as dt
from utils import *
from constants import *


class DirectPing:
    def __init__(self, conn):
        self.conn = conn
        send(conn, ACK_MSG)

    def run(self):
        while True:
            receive(self.conn, PACKAGE_BYTES)
            send(self.conn, ACK_MSG)


class ReversePing:
    def __init__(self, conn):
        self.conn = conn
        send(conn, ACK_MSG)
        self.count = int(receive(conn, COUNT_LEN_BYTES))

    def run(self):
        for i in range(self.count):
            initial_dt = dt.now()
            send(self.conn, get_random_string(PACKAGE_BYTES))
            receive(self.conn, ACK_MSG)
            final_dt = dt.now()

            delta = final_dt - initial_dt
            if delta.seconds >= TIMEOUT_SECONDS:
                send(self.conn, DISCARDED_PCK_RTT)
                continue

            delta = round((delta.seconds + delta.microseconds / 1000000.0) * 1000, 1)
            delta = "{:07.1f}".format(delta)
            send(self.conn, delta)


class ProxyPing:
    def __init__(self, conn):
        self.conn = conn

    def run(self):
        pass
