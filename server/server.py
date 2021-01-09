import asyncio
import logging

import websockets

from game.board import Board


async def handle(websocket, path):
    b = Board()
    while True:
        r = await websocket.recv()
        await websocket.send(b.json_encode())


def run_server():
    logging.info("running server")

    start_server = websockets.serve(handle, "localhost", 5000)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
