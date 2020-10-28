import argparse
from server.server import Server


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("-H", "--host", default="127.0.0.1")
    parser.add_argument("-P", "--port", type=int, default="8080")

    return parser.parse_args()


def main():
    args = parse_arguments()
    address = (args.host, args.port)
    sv = Server(address)
    sv.run()


if __name__ == "__main__":
    main()
