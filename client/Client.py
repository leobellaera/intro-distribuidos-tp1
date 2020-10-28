import socket
from datetime import datetime as dt

from client.output_manager import OutputManager
from constants import DIRECT_PING, PACKAGE_BYTES, ACK_MSG, TIMEOUT_SECONDS
from utils import send, receive, get_random_string


class Client:

    def __init__(self, ip, port):
        """
        Receives an IP and port and creates a connection with a server
        """
        server_address = (ip, port)
        self.out_mgr = OutputManager()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(server_address)
        name = socket.gethostname()
        self.address = socket.gethostbyname(name)
        self.dest_address = ip

    def close(self):
        self.sock.close()

    def direct_ping(self, count):
        """
        Executes direct ping count times and prints output
        """

        # Handshake
        send(self.sock, DIRECT_PING)
        rcv = receive(self.sock, 2)
        if rcv != ACK_MSG:
            raise ValueError(str.format("Expected %s, received %s",
                                        (ACK_MSG, rcv)))

        self.out_mgr.print_file_version()
        self.out_mgr.print_operation(True, False, False)
        self.out_mgr.print_server(self.dest_address)
        self.out_mgr.print_client(self.address)

        # direct ping
        lost = 0
        rtt_list = []
        for i in range(count):
            before = dt.now()
            send(self.sock, get_random_string(PACKAGE_BYTES))
            rcv = receive(self.sock, 2)
            delta = dt.now() - before

            if rcv != ACK_MSG:
                raise ValueError(f"Expected {ACK_MSG}, received {rcv}")

            delta = (delta.seconds + delta.microseconds / 1000000.0) * 1000
            rtt_list.append(delta)
            self.out_mgr.print_latest_message(PACKAGE_BYTES,
                                              self.dest_address, i+1, delta)
            if delta >= TIMEOUT_SECONDS*1000:
                lost += 1
        self.out_mgr.print_statistics(self.dest_address, count, count-lost,
                                      rtt_list)
