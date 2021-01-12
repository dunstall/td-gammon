# Copyright 2021 Andrew Dunstall

import json

from game.player import Player


class WebSocketPlayer(Player):
    def __init__(self, websocket):
        self._websocket = websocket

    async def turn(self, board):
        await self._send_state(board)

        while True:
            msg = await self._websocket.recv()
            payload = json.loads(msg)

            # TODO(AD) Handle inputs (state machine of not rolled,
            # moves remaining, done...)

        rolls = []
        await self._send_state(board, rolls)

    async def _send_state(self, board, rolls=None):
        state = {
            "board": board.state(),
            "rolls": rolls
        }
        await self._websocket.send(json.dumps(state))
