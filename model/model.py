# Copyright 2021 Andrew Dunstall

import random

import numpy as np

from game.backgammon import Backgammon
from game.board import PLAYER_BLACK, PLAYER_WHITE
from game.td_gammon_player import TDGammonPlayer


class Model:
    def __init__(self):
        pass

    async def train(self, n_episodes=1):
        for episode in range(n_episodes):
            game = Backgammon(
                TDGammonPlayer(self, PLAYER_WHITE),
                TDGammonPlayer(self, PLAYER_BLACK)
            )
            await game.play()

    def action(self, board, roll, color):
        permitted = board.permitted_moves(roll, color)
        if len(permitted) == 0:
            return None
        return random.choice(permitted)

        # TODO(AD)
        """
        max_move = None
        max_prob = -np.inf
        for move in board.permitted_moves(roll):
            # TODO(AD) apply should not update board but return a copy with
            # the move applied.
            afterstate = board.apply(move)

            prob = self._model.predict(afterstate)
            if prob > max_prob:
                max_move = move

        return max_move
        """




