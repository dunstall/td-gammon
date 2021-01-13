# Copyright 2021 Andrew Dunstall

import copy
import logging
import random

import numpy as np
import tensorflow as tf

from game.backgammon import Backgammon
from game.board import PLAYER_BLACK, PLAYER_WHITE
from game.td_gammon_player import TDGammonPlayer


class Model:
    def __init__(self):
        inputs = tf.keras.Input(shape=(198,))
        x = tf.keras.layers.Dense(32, activation="relu")(inputs)
        outputs = tf.keras.layers.Dense(1, activation="sigmoid")(x)
        self._model = tf.keras.Model(inputs=inputs, outputs=outputs)

    async def train(self, n_episodes=1):
        for episode in range(n_episodes):
            game = Backgammon(
                TDGammonPlayer(self, PLAYER_WHITE),
                TDGammonPlayer(self, PLAYER_BLACK)
            )
            await game.play()

    def action(self, board, roll, color):
        max_move = None
        max_prob = -np.inf
        for move in board.permitted_moves(roll, color):
            # TODO(AD) Very inefficient
            board_afterstate = copy.deepcopy(board)
            if not board_afterstate.move(*move, color):
                logging.error("model requested an invalid move")
                continue
            prob = self._model.predict(board_afterstate.encode_state(color)[np.newaxis])[0][0]

            if prob > max_prob:
                max_prob = prob
                max_move = move

        print(color, "playing move", max_move, "prob:", max_prob)
        return max_move
