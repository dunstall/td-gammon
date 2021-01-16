# Copyright 2021 Andrew Dunstall

import logging

from game.agent import Agent


class TDGammonAgent(Agent):
    def __init__(self, model, player):
        self._model = model
        self._player = player

    def turn(self, board):
        roll = self._roll()

        while True:
            if len(roll) == 0:
                return

            move = self._model.action(board, roll, self._player)
            # When no moves remaining end the turn.
            if move is None:
                return

            if not board.move(*move, self._player):
                logging.error("td-gammon player requested invalid move")
                continue

            del roll[roll.index(move[1])]

    def update(self, board):
        self._model.update(board, self._player)
