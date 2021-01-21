# Copyright 2021 Andrew Dunstall

import random
import logging

from game.agent import Agent


class RandomAgent(Agent):
    def __init__(self, player):
        self._player = player

    def turn(self, board):
        rolls = self._roll()

        while len(rolls) > 0:
            permitted = board.permitted_moves(rolls, self._player)
            if len(permitted) == 0:
                return

            move = random.choice(permitted)
            if not board.move(*move, self._player):
                logging.error("td-gammon player requested invalid move")
                continue

            del rolls[rolls.index(move[1])]

    def update(self, board):
        pass
