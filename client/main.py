import argparse
import sys

from client.client import Client


def parse_arguments():
    parser = argparse.ArgumentParser(description='<Poner una descripción>')

    v_group = parser.add_mutually_exclusive_group()
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

    p_group = parser.add_mutually_exclusive_group()
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
                        metavar='')  # todo: set COUNT on usage

    parser.add_argument("-d",
                        "--dest",
                        help="destination IP address",
                        dest="dest",
                        metavar='')  # todo: set ADDR on usage

    return parser.parse_args()


def main():
    args = parse_arguments()
    split = args.server.split(":")
    if len(split) != 2 and split[1].isdigit():
        raise ValueError("Invalid server Address")
    try:
        cli = Client(split[0], int(split[1]))
        if args.ping is not None:
            cli.direct_ping(args.count)
        cli.close()
    except ConnectionRefusedError as e:
        print(f"Unable to connect to server: {str(e)}", file=sys.stderr)


if __name__ == "__main__":
    main()
