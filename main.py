import logging

from server.server import run_server


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_server()
