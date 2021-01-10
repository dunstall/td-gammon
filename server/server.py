# Copyright 2021 Andrew Dunstall

import asyncio
import logging
import json

import websockets

from game.board import Board


async def handle(websocket, path):
    b = Board()

    state = b.state()
    msg = {
        "type": "eventMatchStart",
        "state": state
    }

    await websocket.send(json.dumps(msg))
    while True:
        r = await websocket.recv()

        #  payload = json.loads(r)
        #  print(payload)

        #  if payload["type"] == "rollDice":
            #  print("sending roll dice")
            #  json.loads(b.json_encode_roll())
            #  await websocket.send(b.json_encode_roll())

        #  if payload["type"] == "movePiece":
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
