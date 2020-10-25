# Intro-Distribuidos-TP1


## Dependencies

- `sudo apt update`
- `sudo apt install python3-pip`
- `pip3 install -r requirements.txt`

## Workflow

- Run `flake8` command inside project folder
- Commit

## Test
Test with netcat

### Ping
```shell script
$ nc 127.0.0.1 8080
Cli: 01asdfghjklpoiuytrewqasdfghjklmnbvcxzasdfghjklopiuhygtfrdeswaqsd
Srv: 02
```
# Server Ping
```shell script
$ nc 127.0.0.1 8080
Cli: 030002
Srv: 01asdfghjklpoiuytrewqasdfghjklmnbvcxzasdfghjklopiuhygtfrdeswaqsd
Cli: 02
Srv: 01asdfghjklpoiuytrewqasdfghjklmnbvcxzasdfghjklopiuhygtfrdeswaqsd
Cli: 02
Srv: 040516400363
```