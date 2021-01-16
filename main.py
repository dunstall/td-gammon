# Copyright 2021 Andrew Dunstall

import argparse
import asyncio
import logging

from model.model import Model
from server.server import Server


def parse_args():
    parser = argparse.ArgumentParser(description="TD-Gammon model.")
    parser.add_argument(
        "--serve", action='store_true', help="run websocket server"
    )
    parser.add_argument(
        "--debug", action='store_true', help="debug logging"
    )
    return parser.parse_args()


def main(args):
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)

    m = Model()
    if args.serve:
        s = Server(m).listen()
    else:
        asyncio.run(m.train())


if __name__ == "__main__":
    main(parse_args())
