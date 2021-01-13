# Copyright 2021 Andrew Dunstall

import json
import logging

from game.player import Player


class WebSocketPlayer(Player):
    def __init__(self, websocket, color):
        self._websocket = websocket
        self._color = color

    async def turn(self, board):
        roll = self._roll()

        while True:
            await self._send_state(board, roll)

            if len(roll) == 0:
                return

            permitted = board.permitted_moves(roll, self._color)
            if len(permitted) == 0:
                return

            msg = await self._websocket.recv()
            payload = json.loads(msg)

            if "position" not in payload or "steps" not in payload:
                logging.info("invalid request payload")
                continue

            if not board.move(payload["position"], payload["steps"], self._color):
                logging.info("websocket player requested invalid move")
                continue

            del roll[roll.index(payload["steps"])]

    def won(self):
        # TODO(AD) Send to player
        print("won", self._color)

    def lost(self):
        # TODO(AD) Send to player
        print("lost", self._color)

    async def _send_state(self, board, roll):
        state = {
            "board": board.state(),
            "roll": roll
        }
        await self._websocket.send(json.dumps(state))
