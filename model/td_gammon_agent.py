# Copyright 2021 Andrew Dunstall

import logging

from game.agent import Agent
from game.board import PLAYER_O, PLAYER_X


class TDGammonAgent(Agent):
    def __init__(self, model, color):
        self._model = model
        self._color = color

    async def turn(self, board):
        roll = self._roll()

        while True:
            if len(roll) == 0:
                return

            move = self._model.action(board, roll, self._color)
            # When no moves remaining end the turn.
            if move is None:
                return

            if not board.move(*move, self._color):
                logging.error("td-gammon player requested invalid move")
                continue

            del roll[roll.index(move[1])]

    def won(self):
        # TODO(AD) Update model
        print("won", self._color)

    def lost(self):
        # TODO(AD) Update model
        print("lost", self._color)
