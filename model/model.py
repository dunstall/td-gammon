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

    def train(self, n_episodes=5000, n_validation = 500):
        logging.info(f"training model [n_episodes = {n_episodes}]")
        wins = [0, 0]
        for episode in range(1, n_episodes + 1):
            if episode % n_validation == 0:
                self.test()

            player = random.randint(0, 1)
            game = Game(
                TDGammonAgent(self, player),
                TDGammonAgent(self, 1 - player)
            )
            game.play()

            if game.won(player):
                wins[player] += 1
            else:
                wins[1 - player] += 1
            logging.info(f"game complete [wins {wins}] [episodes {episode}]")

            # Reset the trace to zero.
            for i in range(len(self._trace)):
                self._trace[i].assign(tf.zeros(self._trace[i].get_shape()))

    def test(self, n_episodes=100):
        logging.info(f"testing model [n_episodes = {n_episodes}]")
        wins = 0
        for episode in range(1, n_episodes + 1):
            player = random.randint(0, 1)
            game = Game(
                # TODO(AD) Disable training?
                TDGammonAgent(self, player),
                RandomAgent(1 - player)
            )
            game.play()

            if game.won(player):
                wins += 1
            logging.info(f"game complete [model wins {wins}] [episodes {episode}]")

    def action(self, board, roll, player):
        max_move = None
        max_prob = -np.inf
        start = time.time()
        permitted = board.permitted_moves(roll, player)
        for move in permitted:
            afterstate = copy.deepcopy(board)
            if not afterstate.move(*move, player):
                logging.error("model requested an invalid move")
                continue

            state = afterstate.encode_state(player)[np.newaxis]
            prob = tf.reduce_sum(self._model(state))
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
