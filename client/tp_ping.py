import argparse
import sys
from socket import gaierror

from client.client import Client
from common.exceptions import ConnectionClosedException


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='A useful tool to measure latency between two end-hosts')

    v_group = parser.add_mutually_exclusive_group(required=True)
    v_group.add_argument("-v",
                         "--verbose",
                         help="increase output verbosity",
                         action='store_true')
    v_group.add_argument("-q",
                         "--quiet",
                         help="decrease output verbosity",
                         action='store_true')

    parser.add_argument("-s",
                        "--server",
                        help="server ip address",
                        dest="server",
                        metavar='',
                        required=True)

    p_group = parser.add_mutually_exclusive_group(required=True)
    p_group.add_argument("-p",
                         "--ping",
                         help="direct ping",
                         action='store_true')
    p_group.add_argument("-r",
                         "--reverse",
                         help="reverse ping",
                         action='store_true')
    p_group.add_argument("-x",
                         "--proxy",
                         help="proxy ping",
                         action='store_true')

    parser.add_argument("-c",
                        "--count",
                        help="stop after <count> repplies",
                        dest="count",
                        type=int,
                        default=4,
                        metavar='')

    parser.add_argument("-d",
                        "--dest",
                        help="destination IP address",
                        dest="dest",
                        metavar='')

    return parser.parse_args()


def main():
    args = parse_arguments()

    if args.count not in range(1000000):
        print("Bad number of packets to transmit.", file=sys.stderr)
        return

    try:
        cli = Client(args.server, args.count, args.verbose, args.dest)
        if args.ping:
            cli.run_direct_ping()
        elif args.reverse:
            cli.run_reverse_ping()
        else:
            if not args.dest:
                print("Destination ip and port needed", file=sys.stderr)
                return
            elif args.dest and len(args.dest.split(':')) != 2:
                print("Destination ip must be likely <ip>:<port>",
                      file=sys.stderr)
                return
            cli.run_proxy_ping()
        cli.close()
    except (gaierror, ConnectionRefusedError) as e:
        print(f"Unable to connect to server: {str(e)}", file=sys.stderr)
    except ConnectionClosedException as e:
        print(f"Connection Closed: {str(e)}", file=sys.stderr)


if __name__ == "__main__":
    main()
