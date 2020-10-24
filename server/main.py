import argparse
import socket

from server.ConnectionClosedException import ConnectionClosedException


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("-H", "--host", default="127.0.0.1")
    parser.add_argument("-P", "--port", type=int, default="8080")

    return parser.parse_args()


def receive(conn, bytes):
    count = 0
    data = ""
    while count < bytes:
        buf = conn.recv(bytes - count)
        if len(buf) == 0:
            raise ConnectionClosedException('Expected %d, received %d' % (bytes, count))
        count = count + len(buf)
        data = data + buf.decode()
    return data

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
        try:
            if receive(conn, 2) == '01':
                data = receive(conn, 62)
                conn.send(b'02')
        except ConnectionClosedException as e:
            print("Invalid data received: " + str(e))
    sock.close()


if __name__ == "__main__":
    main()
