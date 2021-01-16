# Copyright 2021 Andrew Dunstall

import logging
import random
import time

from game.board import Board


class Game:
    def __init__(self, agent1, agent2):
        self._agents = [agent1, agent2]
        self._board = Board()

    def won(self, player):
        return self._board.won(player)

    async def play(self):
        start = time.time()

        turn = random.randint(0, 1)
        logging.debug(f"game started [player = {turn}]")
        while not self._board.won(turn):
            turn = 1 - turn

            await self._agents[turn].turn(self._board)
            self._agents[turn].update(self._board)

        duration = time.time() - start
        logging.debug(f"game complete [duration = {duration}s], [winner = {turn}]")
