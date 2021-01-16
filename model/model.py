# Copyright 2021 Andrew Dunstall

import copy
import logging
import random
import time

import numpy as np
import tensorflow as tf

from game.game import Game
from game.random_agent import RandomAgent
from model.td_gammon_agent import TDGammonAgent


class Model:
    def __init__(self):
        inputs = tf.keras.Input(shape=(198,))
        x = tf.keras.layers.Dense(32, activation="relu")(inputs)
        outputs = tf.keras.layers.Dense(1, activation="sigmoid")(x)
        self._model = tf.keras.Model(inputs=inputs, outputs=outputs)

        self._trace = []
        # TODO(AD) Decay
        self._lambda = 0.9
        self._alpha = 0.1

        self._x = None
        self._V = None

    async def train(self, n_episodes=1):
        for episode in range(n_episodes):
            player = random.randint(0, 1)
            game = Game(
                TDGammonAgent(self, player),
                TDGammonAgent(self, 1 - player)
            )
            await game.play()

    async def test(self, n_episodes=100):
        wins = 0
        for episode in range(1, n_episodes + 1):
            player = random.randint(0, 1)
            game = Game(
                TDGammonAgent(self, player),
                RandomAgent(1 - player)
            )
            await game.play()

            if game.won(player):
                wins += 1
            logging.info(f"game complete [model wins {wins}] [episodes {episode}]")

    def action(self, board, roll, player):
        max_move = None
        max_prob = -np.inf
        start = time.time()
        for move in board.permitted_moves(roll, player):
            # TODO(AD) Very inefficient - use apply and undo
            afterstate = copy.deepcopy(board)
            if not afterstate.move(*move, player):
                logging.error("model requested an invalid move")
                continue
            prob = self._model.predict(afterstate.encode_state(player)[np.newaxis])[0][0]
            if prob > max_prob:
                max_prob = prob
                max_move = move

        if self._x is None:
            self._x = board.encode_state(player)
        if self._V is None:
            self._V = self._model(self._x[np.newaxis])

        duration = time.time() - start
        logging.debug(f"playing move [player = {player}] [move = {max_move}] [winning prob = {max_prob}] [duration = {duration}s]")
        return max_move

    def update(self, board, player):
        start = time.time()
        x_next = board.encode_state(player)

        with tf.GradientTape() as tape:
            V_next = self._model(x_next[np.newaxis])

        tvars = self._model.trainable_variables
        grads = tape.gradient(V_next, tvars)

        if len(self._trace) == 0:
            for grad in grads:
                self._trace.append(tf.Variable(
                    tf.zeros(grad.get_shape()), trainable=False
                ))

        reward = 1 if board.won(player) else 0

        delta = tf.reduce_sum(reward + V_next - self._V)
        for i in range(len(grads)):
            self._trace[i].assign((self._lambda * self._trace[i]) + grads[i])

            grad_trace = self._alpha * delta * self._trace[i]
            self._model.trainable_variables[i].assign_add(grad_trace)

        self._x = x_next
        self._V = V_next

        duration = time.time() - start
        logging.debug(f"updating model [player = {player}] [duration = {duration}s]")
