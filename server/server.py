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

    while True:
        r = await websocket.recv()
        payload = json.loads(r)

        if payload["type"] == "rollDice":
            resp = {"type": "rollDice", "roll": game.roll()}
            await websocket.send(json.dumps(resp))


        # TODO(AD)
        # 1 Wait for clicking 'roll'            RECV
        # 2 Send rollDice and permitted moves   SEND
        # 3 Recv move                           RECV
        # 4 game.move(move)
        # 5 Send updated state (after AI move too)  SEND
        # 6 Repeat.





        if payload["type"] == "movePiece":
            print(payload)
            game.move(payload["position"], payload["steps"])

            # TODO handle invalid move

            # TODO AI play its move before sending state

            msg = {
                "type": "eventMatchStart",
                "state": game.board().state()
                # TODO add rolls with one decr?
            }
            await websocket.send(json.dumps(msg))


        #  {'position': 12, 'steps': 5, 'clientMsgSeq': None, 'type': 'movePiece'}

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
