BACKLOG = 1

PING_BYTES = 1  # ping type
ACK_BYTES = 2   # ok - er
PACKAGE_BYTES = 64  # ping message
RTT_BYTES = 7  # rtt time
DEST_ADDR_LEN_BYTES = 4  # DEST ip and port len
COUNT_LEN_BYTES = 4

DIRECT_PING = "d"
REVERSE_PING = "r"
PROXY_PING = "p"

ACK_MSG = "ok"
ERR_MSG = "er"

TIMEOUT_SECONDS = 30
DISCARDED_PCK_RTT = "30000.0"
