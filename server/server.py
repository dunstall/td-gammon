# Copyright 2021 Andrew Dunstall

import asyncio
import logging
import json

import websockets

from game.backgammon import Backgammon


async def handle(websocket, path):
    game = Backgammon()

    # Send match start.
    msg = {
        "type": "eventMatchStart",
        "state": game.board().state()
    }
    await websocket.send(json.dumps(msg))

    # Each round of the episode.
    while True:
        r = await websocket.recv()

        # TODO(AD)
        # 1 Wait for clicking 'roll'            RECV
        # 2 Send rollDice and permitted moves   SEND
        # 3 Recv move                           RECV
        # 4 game.move(move)
        # 5 Send updated state (after AI move too)  SEND
        # 6 Repeat.

        payload = json.loads(r)
        print(payload)

        if payload["type"] == "rollDice":
            print("sending roll dice")
            #  json.loads(b.json_encode_roll())
            resp = {"type": "rollDice", "roll": [5, 1]}
            await websocket.send(json.dumps(resp))

        #  if payload["type"] == "movePiece":
            # TODO(AD) game.move(...)

            #  print("sending move pience")
            #  json.loads(b.json_encode2())
            #  await websocket.send(b.json_encode2())

        # TODO once player moved get the 'AI' to play its turn
        # send eventPieceMove for each move
        # then eventTurnStart



def run_server():
    logging.info("running server")

    start_server = websockets.serve(handle, "localhost", 5000)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
