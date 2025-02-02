import socket
import sys
from datetime import datetime as dt

from client.output_manager import OutputManager
from common.constants import DIRECT_PING, PACKAGE_LEN, \
    ACK_MSG, TIMEOUT_SECONDS, ACK_LEN, SV_PORT, COUNT_LEN, \
    RTT_LEN, DISCARDED_PCK_RTT, REVERSE_PING, PROXY_PING, DEST_ADDR_LEN
from common.exceptions import ConnectionClosedException
from common.utils import send, receive, get_random_string


class Client:

    def __init__(self, ip, count, verbose, proxy_address=None):
        """
        Receives an IP and creates a connection with a ping server
        """
        self.count = count
        self.verbose = verbose
        self.proxy_address = proxy_address

        self.out_mgr = OutputManager()
        server_address = (ip, SV_PORT)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(server_address)
        name = socket.gethostname()
        self.address = socket.gethostbyname(name)
        self.dest_address = ip

    def close(self):
        self.sock.close()

    def run_direct_ping(self):
        """
        Executes direct ping count times and prints output
        """

        # handshaking
        send(self.sock, DIRECT_PING)
        rcv = receive(self.sock, ACK_LEN)
        if rcv != ACK_MSG:
            raise ValueError(str.format("Expected %s, received %s",
                                        (ACK_MSG, rcv)))

        self.out_mgr.print_file_version()
        self.out_mgr.print_operation(True, False, False)
        self.out_mgr.print_server(self.dest_address)
        self.out_mgr.print_client(self.address)

        # direct ping
        packet_loss = 0
        rtt_list = []
        for i in range(self.count):
            before = dt.now()
            send(self.sock, get_random_string(PACKAGE_LEN))
            rcv = receive(self.sock, ACK_LEN)
            delta = dt.now() - before

            if rcv != ACK_MSG:
                raise ValueError(f"Expected {ACK_MSG}, received {rcv}")

            delta = round((delta.seconds + delta.microseconds / 1000000.0) *
                          1000, 1)

            if delta >= (TIMEOUT_SECONDS * 1000):
                packet_loss += 1
                continue

            rtt_list.append(delta)
            if self.verbose:
                self.out_mgr.print_latest_message(
                    PACKAGE_LEN, self.dest_address, i + 1, delta)

        self.out_mgr.print_statistics(self.dest_address, self.count,
                                      self.count - packet_loss, rtt_list)

    def run_reverse_ping(self):
        """
        Executes reverse ping count times and prints output
        """

        # handshaking
        send(self.sock, REVERSE_PING)
        sig = receive(self.sock, ACK_LEN)
        if sig != ACK_MSG:
            raise ValueError(str.format("Expected %s, received %s",
                                        (ACK_MSG, sig)))

        _format = '0' + str(COUNT_LEN) + 'd'
        send(self.sock, format(self.count, _format))

        self.out_mgr.print_file_version()
        self.out_mgr.print_operation(False, True, False)
        self.out_mgr.print_server(self.dest_address)
        self.out_mgr.print_client(self.address)

        packet_loss = 0
        rtt_list = []

        for i in range(self.count):
            try:
                receive(self.sock, PACKAGE_LEN)
                send(self.sock, ACK_MSG)
                rtt = float(receive(self.sock, RTT_LEN))

                if rtt == DISCARDED_PCK_RTT:
                    packet_loss += 1
                    continue

                rtt_list.append(rtt)
                if self.verbose:
                    self.out_mgr.print_latest_message(
                        PACKAGE_LEN, self.dest_address, i + 1, rtt)
            except ConnectionClosedException:
                break

        self.out_mgr.print_statistics(self.dest_address, self.count,
                                      self.count - packet_loss, rtt_list)

    def run_proxy_ping(self):
        """
        Executes proxy ping count times and prints output
        """

        # handshaking
        send(self.sock, PROXY_PING)

        format_count = '0' + str(COUNT_LEN) + 'd'
        send(self.sock, format(self.count, format_count))

        format_dest_addr = '0' + str(DEST_ADDR_LEN) + 'd'
        send(self.sock, format(len(self.proxy_address), format_dest_addr))
        send(self.sock, self.proxy_address)

        sig = receive(self.sock, ACK_LEN)
        if sig != ACK_MSG:
            print("Unable to connect to proxy server", file=sys.stderr)
            return

        self.out_mgr.print_file_version()
        self.out_mgr.print_operation(False, False, True)
        self.out_mgr.print_server(self.dest_address)
        self.out_mgr.print_client(self.address)

        packet_loss = 0
        rtt_list = []
        for i in range(self.count):
            _sig = receive(self.sock, ACK_LEN)
            if _sig != ACK_MSG:
                print("Connection between server and proxy ended " +
                      "unexpectedly", file=sys.stderr)
                return

            rtt = float(receive(self.sock, RTT_LEN))

            if rtt == DISCARDED_PCK_RTT:
                packet_loss += 1
                continue

            rtt_list.append(rtt)
            if self.verbose:
                self.out_mgr.print_latest_message(
                    PACKAGE_LEN, self.dest_address, i + 1, rtt)

        self.out_mgr.print_statistics(self.dest_address, self.count,
                                      self.count - packet_loss, rtt_list)
