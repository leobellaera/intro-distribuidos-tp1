import argparse
import socket


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("-H", "--host", default="127.0.0.1")
    parser.add_argument("-P", "--port", type=int, default="8080")

    return parser.parse_args()


def main():
    args = parse_arguments()
    address = (args.host, args.port)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(address)
    sock.listen(1)

    while True:
        conn, addr = sock.accept()
        if not conn:
            break

        if conn.recv(1).decode() == 'c':
            conn.send(b's')

    sock.close()


if __name__ == "__main__":
    main()
