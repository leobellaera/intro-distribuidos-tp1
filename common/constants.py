BACKLOG = 1
SV_PORT = 8080

PING_TYPE_LEN = 1  # ping type ('r', 'd' or 'p') length in bytes
ACK_LEN = 2   # ack length in bytes
PACKAGE_LEN = 64  # ping package length in bytes
RTT_LEN = 7  # rtt time length in bytes
DEST_ADDR_LEN = 3  # destination ip-port length in bytes
COUNT_LEN = 6  # count length in bytes

DIRECT_PING = "d"
REVERSE_PING = "r"
PROXY_PING = "p"

ACK_MSG = "ok"
ERR_MSG = "er"

TIMEOUT_SECONDS = 30
DISCARDED_PCK_RTT = 30000.0  # milliseconds
