PING_BYTES = 1  # ping type
ACK_BYTES = 2   # ok - er
DATA_BYTES = 64 # ping message
RTT_BYTES = 8 # rtt time
DEST_ADDR_LEN_BYTES = 4 # DEST ip and port len
COUNT_LEN_BYTES = 4

DIRECT_PING = "d"
REVERSE_PING = "r"
PROXY_PING = "p"

MESSAGE_OK = "ok"
ERROR_OK = "er"

TIMEOUT_SECONDS = 30