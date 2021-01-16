# Copyright 2021 Andrew Dunstall

import logging
import random

from game.board import Board


class Game:
    def __init__(self, agent1, agent2):
        self._agents = [agent1, agent2]
        self._board = Board()

    async def play(self):
        turn = random.randint(0, 1)
        while not self._board.won(turn):
            turn = 1 - turn
            await self._agents[turn].turn(self._board)

        self._agents[turn].won()
        self._agents[1 - turn].lost()
