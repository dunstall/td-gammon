# Copyright 2021 Andrew Dunstall

import argparse
import asyncio
import logging

from server.server import run_server
from ai.model import Model


ACTION_TRAIN = "train"
ACTION_SERVE = "serve"


def parse_args():
    parser = argparse.ArgumentParser(description="TD-Gammon model.")
    parser.add_argument(
        "action", choices=[ACTION_TRAIN, ACTION_SERVE], help="TD-Gammon action"
    )
    return parser.parse_args()


def main(args):
    logging.basicConfig(level=logging.INFO)

    m = Model()
    if args.action == ACTION_TRAIN:
        asyncio.run(m.train())
    elif args.action == ACTION_SERVE:
        run_server()


if __name__ == "__main__":
    main(parse_args())
