# Copyright 2021 Andrew Dunstall

import copy
import datetime
import logging
import os
import random
import time

import numpy as np
import tensorflow as tf

from game.game import Game
from game.random_agent import RandomAgent
from model.td_gammon_agent import TDGammonAgent


# TODO(AD) Check save and load same for all params
class Model:
    def __init__(self, restore_path = None):
        inputs = tf.keras.Input(shape=(198,))
        x = tf.keras.layers.Dense(32, activation="relu")(inputs)
        outputs = tf.keras.layers.Dense(1, activation="sigmoid")(x)
        self._model = tf.keras.Model(inputs=inputs, outputs=outputs)

        self._trace = []

        self._step = tf.Variable(0, trainable=False)

        self._lambda_schedule = tf.keras.optimizers.schedules.ExponentialDecay(
            0.9, 30000, 0.96, staircase=True
        )
        self._alpha_schedule = tf.keras.optimizers.schedules.ExponentialDecay(
            0.1, 40000, 0.96, staircase=True
        )

        game = Game(
            TDGammonAgent(self, 0),
            TDGammonAgent(self, 1)
        )
        self._x = tf.Variable(game._board.encode_state(0))
        self._V = tf.Variable(self._model(self._x[np.newaxis]))

        if restore_path is not None:
            self.load(restore_path)

    def lambda_decay(self):
        return tf.maximum(0.7, self._lambda_schedule(self._step))

    def alpha(self):
        return tf.maximum(0.01, self._alpha_schedule(self._step))

    def train(self, n_episodes=5000, n_validation=500, n_checkpoint=500):
        logging.info(f"training model [n_episodes = {n_episodes}]")
        wins = [0, 0]
        for episode in range(1, n_episodes + 1):
            if episode % n_validation == 0:
                self.test()
            if episode > 1 and episode % n_checkpoint == 0:
                self.save()

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

            self._step.assign_add(1)

        self.save()

    def test(self, n_episodes):
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

        logging.info(f"test complete [ratio {wins/n_episodes}]")

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
            # Reward is 1 if player 2 wins, 0 otherwise. So player 1 is trying
            # to minimize prob.
            # TODO(AD) Refactor
            prob = 1 - prob if player == 0 else prob
            if prob > max_prob:
                max_prob = prob
                max_move = move

        if self._x is None:
            self._x = tf.Variable(board.encode_state(player))
        if self._V is None:
            self._V = tf.Variable(self._model(self._x[np.newaxis]))

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

        #  reward = 1 if board.won(player) else 0
        # TODO(AD) Switch to 1 if white won.
        # TODO(AD) Refactor
        if player == 1 and board.won(player):
            reward = 1
        else:
            reward = 0

        delta = tf.reduce_sum(reward + V_next - self._V)
        for i in range(len(grads)):
            self._trace[i].assign((self.lambda_decay() * self._trace[i]) + grads[i])

            grad_trace = self.alpha() * delta * self._trace[i]
            self._model.trainable_variables[i].assign_add(grad_trace)

        self._x = tf.Variable(x_next)
        self._V = tf.Variable(V_next)

        duration = time.time() - start
        logging.debug(f"updating model [player = {player}] [duration = {duration}s]")

    def load(self, path):
        logging.info(f"loading checkpoint [path = {path}]")

        ckpt = tf.train.Checkpoint(model=self._model, step=self._step, x=self._x, V=self._V)
        ckpt.restore(path)

    def save(self):
        if not os.path.exists('checkpoint'):
            os.mkdir('checkpoint')

        directory = 'checkpoint/model-' + str(datetime.datetime.now()).replace(' ', '_')
        if not os.path.exists(directory):
            os.mkdir(directory)

        ckpt = tf.train.Checkpoint(model=self._model, step=self._step, x=self._x, V=self._V)
        path = ckpt.save(directory)

        logging.info(f"saving checkpoint [path = {path}]")

        return path

