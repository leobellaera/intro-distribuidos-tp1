import random
import string

from server.ConnectionClosedException import ConnectionClosedException


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


def receive(conn, n):
    """
    Receives fixed length bytes from socket conn and returns decoded data as
    str
    """

    count = 0
    data = ""
    while count < n:
        buf = conn.recv(n - count)
        if len(buf) == 0:
            s = 'Expected %d, received %d' % (n, count)
            raise ConnectionClosedException(s)
        count = count + len(buf)
        data = data + buf.decode()
    return data


def get_random_string(length):
    """
    Returns random string with fixed length <length>
    """

    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))
