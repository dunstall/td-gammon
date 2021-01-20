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
        x = tf.keras.layers.Dense(40, activation="sigmoid")(inputs)
        outputs = tf.keras.layers.Dense(1, activation="sigmoid")(x)
        self._model = tf.keras.Model(inputs=inputs, outputs=outputs)

        self._trace = []

        self._step = tf.Variable(0, trainable=False)
        # TODO(AD) alpha  = 0.1 and lambda = 0.7. ? from paper
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
        self._state = tf.Variable(game._board.encode_state(0))
        self._value = tf.Variable(self._model(self._state[np.newaxis]))

        if restore_path is not None:
            self.load(restore_path)

    def train(self, n_episodes=5000, n_validation=500, n_checkpoint=500, n_tests=1000):
        logging.info("training model [n_episodes = %d]", n_episodes)
        wins = [0, 0]
        for episode in range(1, n_episodes + 1):
            if episode % n_validation == 0:
                self.test(n_tests)
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
            logging.info("game complete [wins %d] [episodes %d]", wins, episode)

            # Reset the trace to zero after each episode.
            for i in range(len(self._trace)):
                self._trace[i].assign(tf.zeros(self._trace[i].get_shape()))

            self._step.assign_add(1)

        self.save()

    def test(self, n_episodes):
        logging.info("testing model [n_episodes = %d]", n_episodes)
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
            logging.info("game complete [model wins %d] [episodes %d]", wins, episode)

        logging.info("test complete [ratio %f]", wins/n_episodes)

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
            prob = 1 - prob if player == 1 else prob
            if prob > max_prob:
                max_prob = prob
                max_move = move

        if self._state is None:
            self._state = tf.Variable(board.encode_state(player))
        if self._value is None:
            self._value = tf.Variable(self._model(self._state[np.newaxis]))

        duration = time.time() - start
        logging.debug("playing move [player = %d] [move = %s] [winning prob = %f] [duration = %ds]", player, str(max_move), max_prob, duration)
        return max_move

    def update(self, board, player):
        start = time.time()
        x_next = board.encode_state(player)

        with tf.GradientTape() as tape:
            value_next = self._model(x_next[np.newaxis])

        tvars = self._model.trainable_variables
        grads = tape.gradient(value_next, tvars)

        if len(self._trace) == 0:
            for grad in grads:
                self._trace.append(tf.Variable(
                    tf.zeros(grad.get_shape()), trainable=False
                ))

        if player == 0 and board.won(player):
            reward = 1
        else:
            reward = 0

        delta = tf.reduce_sum(reward + value_next - self._value)
        for i in range(len(grads)):
            self._trace[i].assign((self._lambda() * self._trace[i]) + grads[i])

            grad_trace = self._alpha() * delta * self._trace[i]
            self._model.trainable_variables[i].assign_add(grad_trace)

        self._state = tf.Variable(x_next)
        self._value = tf.Variable(value_next)

        duration = time.time() - start
        logging.debug("updating model [player = %d] [duration = %ds]", player, duration)

    def load(self, path):
        logging.info("loading checkpoint [path = %s]", path)

        ckpt = tf.train.Checkpoint(model=self._model, step=self._step, x=self._state, value=self._value)
        ckpt.restore(path)

    def save(self):
        if not os.path.exists('checkpoint'):
            os.mkdir('checkpoint')

        directory = 'checkpoint/model-' + str(datetime.datetime.now()).replace(' ', '_')
        if not os.path.exists(directory):
            os.mkdir(directory)

        ckpt = tf.train.Checkpoint(model=self._model, step=self._step, state=self._state, value=self._value)
        path = ckpt.save(directory)

        logging.info("saving checkpoint [path = %s]", path)

        return path

    def _lambda(self):
        return tf.maximum(0.7, self._lambda_schedule(self._step))

    def _alpha(self):
        return tf.maximum(0.01, self._alpha_schedule(self._step))
