# Copyright 2021 Andrew Dunstall

import asyncio
import logging
import random

import websockets

from game.game import Game
from model.td_gammon_agent import TDGammonAgent
from server.websocket_agent import WebSocketAgent


class Server:
    def __init__(self, model):
        self._model = model

    def listen(self):
        logging.info("running server")

        start_server = websockets.serve(self.handle, "localhost", 5000)

        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

    async def handle(self, websocket, _path):
        logging.info("handle new game")
        player = random.randint(0, 1)
        agent = WebSocketAgent(websocket, player)

        game = Game(agent, TDGammonAgent(self._model, 1 - player))
        await game.play()
