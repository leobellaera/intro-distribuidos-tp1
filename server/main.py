import argparse
import socket

from server.ConnectionClosedException import ConnectionClosedException


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("-H", "--host", default="127.0.0.1")
    parser.add_argument("-P", "--port", type=int, default="8080")

    return parser.parse_args()


def receive(conn, byts):
    """
    Receives fixed length bytes from socket conn and returns decoded data as
    str
    """

    count = 0
    data = ""
    while count < byts:
        buf = conn.recv(byts - count)
        if len(buf) == 0:
            s = 'Expected %d, received %d' % (byts, count)
            raise ConnectionClosedException(s)
        count = count + len(buf)
        data = data + buf.decode()
    return data

def send(conn, data):
    """
    Sends string encoded to socket conn
    """

    total_sent = 0
    length = len(data)
    data = data.encode()
    while total_sent < length:
        count = conn.send(data[total_sent:])
        if count == 0:
            s = 'Conn closed after %d of %d' % (total_sent, length)
            raise ConnectionClosedException(s)
        total_sent = total_sent + count

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
            cmd = receive(conn, 2)
            if cmd == "01":
                receive(conn, 62)
                send(conn, "02")
            elif cmd == "03":
                #count = int(receive(conn, 4))
                #for _ in range(count):
                print("tbd")
        except ConnectionClosedException as e:
            print("Invalid data received: " + str(e))
    sock.close()


if __name__ == "__main__":
    main()
