# Copyright 2021 Andrew Dunstall

import asyncio
import logging
import json

import websockets

from game.backgammon import Backgammon
from game.player import RandomPlayer


async def handle(websocket, path):
    game = Backgammon(RandomPlayer())

    # TODO(AD) randomly select who goes first - if AI then run
    # the move before sending init

    # Send match start.
    msg = game.state()
    msg["type"] = "eventMatchStart"
    await websocket.send(json.dumps(msg))

    while True:
        r = await websocket.recv()
        payload = json.loads(r)

        print(payload)

        if payload["type"] == "rollDice":
            game.roll()
            print("PLAYER ROLL", game._rolls)

            # TODO(AD) if no permiited moves continue to next round
            # TODO(AD) maybe provide notifications for stuff like this

            msg = game.state()
            msg["type"] = "eventMatchStart"
            await websocket.send(json.dumps(msg))

        if payload["type"] == "movePiece":
            if payload["position"] == "bar":
                print("MOVE BAR REQ")

            game.move(payload["position"], payload["steps"])

            # If no permitted moves skip to next round.
            if len(game.permitted_moves()) == 0:
                game.skip()

            msg = game.state()
            msg["type"] = "eventMatchStart"
            await websocket.send(json.dumps(msg))


def run_server():
    logging.info("running server")

    start_server = websockets.serve(handle, "localhost", 5000)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
