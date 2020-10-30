# Intro-Distribuidos-TP1


## Dependencies

- `sudo apt update`
- `sudo apt install python3-pip`
- `pip3 install -r requirements.txt`

## Workflow

- Run `flake8` command inside project folder
- Commit

## Test Client
Test with netcat

### Ping
```shell script
$ nc -l 8080
Cli: d
Srv: ok
Cli: asdfghjklpoiuytrewqasdfghjklmnbvcxzasdfghjklopiuhygtfrdeswaqsd
Srv: ok
Cli: asdfghjklpoiuytrewqasdfghjklmnbvcxzasdfghjklopiuhygtfrdeswaqsd
Srv: ok
Cli: asdfghjklpoiuytrewqasdfghjklmnbvcxzasdfghjklopiuhygtfrdeswaqsd
Srv: ok
Cli: asdfghjklpoiuytrewqasdfghjklmnbvcxzasdfghjklopiuhygtfrdeswaqsd
Srv: ok

OUTPUT:
python3 client/main.py -s 127.0.0.1:8080 -c 4 -p
TP-PING v0.1
Operation: Direct Ping
Server Address: 127.0.0.1
Client Address: 127.0.1.1
64 bytes from 127.0.0.1: seq=1 time=TIMEOUT (>30 secs)
64 bytes from 127.0.0.1: seq=2 time=1671.5 ms
64 bytes from 127.0.0.1: seq=3 time=1664.1 ms
64 bytes from 127.0.0.1: seq=4 time=1319.4 ms

--- 127.0.0.1 ping statistics ---
4 packets transmitted, 3 received, 25 % packet loss, time 40175.6ms
rtt min/avg/max/mdev = 1319.435/10043.896/35520.565/16985.240 ms
```

## Run Commands

### Server 
```shell script
$ python3 -m server.tp_ping_srv
```

### Proxy Server 
```shell script
$ python3 -m server.tp_ping_srv -P 8081
```

### Client - Direct Ping
```shell script
$ python3 -m client.tp_ping -s localhost -c 4 -v -p
```

### Client - Reverse Ping
```shell script
$ python3 -m client.tp_ping -s localhost -c 4 -v -r
```

### Client - Direct Ping
```shell script
$ python3 -m client.tp_ping -s localhost -c 4 -v -x -d 127.0.0.1:8081
```
