import argparse
import sys

from client.client import Client
from common.exceptions import ConnectionClosedException


def parse_arguments():
    parser = argparse.ArgumentParser(description='A useful tool to measure latency between two end-hosts')

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
    try:
        cli = Client(args.server, args.count, args.verbose)
        if args.ping:
            cli.run_direct_ping()
        elif args.reverse:
            cli.run_reverse_ping()
        else:
            pass  # todo proxy
        cli.close()
    except ConnectionRefusedError as e:
        print(f"Unable to connect to server: {str(e)}", file=sys.stderr)
    except ConnectionClosedException as e:
        pass  # todo print error msg
    finally:
        cli.close()


if __name__ == "__main__":
    main()
