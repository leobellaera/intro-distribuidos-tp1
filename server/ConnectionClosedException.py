class ConnectionClosedException(Exception):
    """ Socket closed before receiving expected data"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return 'ConnectionClosedException({0})'.format(str(self.value))
