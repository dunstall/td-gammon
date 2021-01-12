# Copyright 2021 Andrew Dunstall

import asyncio
import logging

import websockets

from game.backgammon import Backgammon
from game.board import PLAYER_BLACK, PLAYER_WHITE
from game.td_gammon_player import TDGammonPlayer
from server.websocket_player import WebSocketPlayer


class Server:
    def __init__(self, model):
        self._model = model

    async def handle(self, websocket, _path):
        logging.info("handle new game")
        player = WebSocketPlayer(websocket, PLAYER_WHITE)

        game = Backgammon(player, TDGammonPlayer(self._model, PLAYER_WHITE))
        await game.play()

    def run(self):
        logging.info("running server")

        start_server = websockets.serve(self.handle, "localhost", 5000)

        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
