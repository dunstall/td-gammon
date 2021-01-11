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

        if payload["type"] == "rollDice":
            game.roll()

            # TODO(AD) if no permiited moves continue to next round

            msg = game.state()
            msg["type"] = "eventMatchStart"
            await websocket.send(json.dumps(msg))

        # TODO(AD) Rules
        # - Handle case no available moves given the roll
        #   for this already need to gen list of permitted moves for AI so
        #   can do this here too - ie if permitted moves empty move on
        # - If only one move available given the roll must pick highest
        # - FE not handling middle of board (hit)
        # - Allow moving from the bar to the board
        # - Cannot move other checkers until all those on bar removed
        # - Bearing off

        if payload["type"] == "movePiece":
            if payload["position"] == "bar":
                print("MOVE BAR REQ")

            game.move(payload["position"], payload["steps"])

            # TODO(AD) if no permiited moves to next round

            msg = game.state()
            msg["type"] = "eventMatchStart"
            await websocket.send(json.dumps(msg))


def run_server():
    logging.info("running server")

    start_server = websockets.serve(handle, "localhost", 5000)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
