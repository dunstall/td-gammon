import asyncio
import logging
import json

import websockets

from game.board import Board


async def handle(websocket, path):
    b = Board()
    await websocket.send(b.json_encode())
    while True:
        r = await websocket.recv()

        payload = json.loads(r)
        print(payload)

        if payload["type"] == "rollDice":
            print("sending roll dice")
            await websocket.send(b.json_encode_roll())

        if payload["type"] == "movePiece":
            print("sending move pience")
            await websocket.send(b.json_encode2())

        # TODO once player moved get the 'AI' to play its turn
        # send eventPieceMove for each move
        # then eventTurnStart



def run_server():
    logging.info("running server")

    start_server = websockets.serve(handle, "localhost", 5000)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

# Use type as first element of list
#  ["eventMatchStart",{"match":{"id":76538953,"host"

#  Sending message movePiece with ID 5
# {"piece":{"type":0,"id":13},"steps":2,"moveSequence":0,"clientMsgSeq":5}

# eventPieceMove
