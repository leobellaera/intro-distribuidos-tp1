import argparse
import socket
from output_manager import OutputManager


def parse_arguments():
    parser = argparse.ArgumentParser(description='<Poner una descripción>')

    v_group = parser.add_mutually_exclusive_group()
    v_group.add_argument("-v",
                         "--verbose",
                         help="increase output verbosity",
                         action='store_true')
    v_group.add_argument("-q",
                         "--quiet",
                         help="decrease output verbosity",
                         action='store_true')

    arg_s = parser.add_argument("-s",
                                "--server",
                                help="server ip address",
                                dest="server")  # todo: set ADDR on usage
    arg_c = parser.add_argument("-c",
                                "--count",
                                help="stop after <count> repplies",
                                dest="count")

    p_group = parser.add_mutually_exclusive_group()
    p_group.add_argument("-p",
                         "--ping",
                         help="direct ping",
                         action='store_true')
    p_group.add_argument("-r",
                         "--reverse",
                         help="reverse ping",
                         action='store_true')
    p_group.add_argument("-x",
                         "--proxy",
                         help="proxy ping",
                         action='store_true')

    arg_d = parser.add_argument("-d",
                                "--dest",
                                help="destination IP address",
                                dest="dest")  # todo: set ADDR on usage

    usage = parser.format_usage()
    parser.usage = usage.replace("usage: ", "")   # grab original usage
    for arg in [arg_s, arg_c, arg_d]:
        arg.metavar = '\b'

    return parser.parse_args()


def main():
    output_manager = OutputManager()
    args = parse_arguments()
    server_address = (args.server, 8080)

    # Create socket and connect to server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    sock.send(b'c')

    signal = sock.recv(1)
    if signal.decode() != "s":
        print("There was an error on the server")
        exit(1)

    print(signal.decode())
    sock.close()


if __name__ == "__main__":
    main()
