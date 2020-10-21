import argparse
import socket


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("-H", "--host", default="127.0.0.1")
    parser.add_argument("-P", "--port", type=int, default="8080")

    return parser.parse_args()


def main():
    args = parse_arguments()
    server_address = (args.host, args.port)

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
