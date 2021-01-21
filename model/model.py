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


class Model:
    """
    Model wraps the neural net and provides methods for training and
    action selection by the agent.
    """
    _LAMBDA = 0.7
    _ALPHA = 0.1

    def __init__(self, restore_path = None):
        """Construct a model with random weights.

        Arguments:
        restore_path -- path to stored checkpoint to restore if given
            (default None)
        """
        inputs = tf.keras.Input(shape=(198,))
        x = tf.keras.layers.Dense(40, activation="sigmoid")(inputs)
        outputs = tf.keras.layers.Dense(1, activation="sigmoid")(x)
        self._model = tf.keras.Model(inputs=inputs, outputs=outputs)

        # Lazily initialize trace once the shape of the gradients is known.
        self._trace = []

        game = Game(
            TDGammonAgent(self, 0),
            TDGammonAgent(self, 1)
        )
        self._state = tf.Variable(game._board.encode_state(0))
        self._value = tf.Variable(self._model(self._state[np.newaxis]))

        if restore_path is not None:
            self.load(restore_path)

    def train(self, n_episodes=5000, n_validation=500, n_checkpoint=500, n_tests=1000):
        """Trains the model.

        Arguments:
        n_episodes -- number of episodes to train (default 5000)
        n_validation -- number of episodes between testing the model
            (default 500)
        n_checkpoint -- number of episodes between saving the model
            (default 500)
        n_tests -- number of episodes to test (default 1000)
        """
        logging.info("training model [n_episodes = %d]", n_episodes)
        for episode in range(1, n_episodes + 1):
            logging.info("running episode [episode = %d]", episode)
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

            self._reset_trace()

        self.save()

    def test(self, n_episodes=100):
        """Tests the model against a random agent.

        Arguments:
        n_episodes -- number of episodes to test (default 100)
        """
        logging.info("testing model [n_episodes = %d]", n_episodes)
        wins = 0
        for episode in range(1, n_episodes + 1):
            player = random.randint(0, 1)
            game = Game(
                TDGammonAgent(self, player),
                RandomAgent(1 - player)
            )
            game.play()

            if game.won(player):
                wins += 1

            logging.info("game complete [model wins %d] [episodes %d]", wins, episode)

        logging.info("test complete [model win ratio %f]", wins/n_episodes)

    def action(self, board, roll, player):
        """Predicts the optimal move given the current state.

        This calculates each afterstate for all possible moves given the
        current state and selects the action that leads to the state with
        the greatest afterstate value.

        Arguments:
        board -- board containing the game state
        roll -- list of dice rolls left in the players turn
        player -- number of the player
        """
        start = time.time()

        max_move = None
        max_prob = -np.inf
        permitted = board.permitted_moves(roll, player)
        for move in permitted:
            afterstate = copy.deepcopy(board)
            if not afterstate.move(*move, player):
                logging.error("model requested an invalid move")
                continue

            state = afterstate.encode_state(player)[np.newaxis]
            prob = tf.reduce_sum(self._model(state))
            # The network gives the probability of player 0 winning so must
            # change if player 1.
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
        """Updates the model given the current state and reward.

        This is expected to be called after the player has made their move.

        The aim is to move the predicted values towards the actual reward
        using TD-lambda.

        Arguments:
        board -- board containing the game state
        roll -- list of dice rolls left in the players turn
        """
        start = time.time()

        x_next = board.encode_state(player)
        with tf.GradientTape() as tape:
            value_next = self._model(x_next[np.newaxis])

        trainable_vars = self._model.trainable_variables
        grads = tape.gradient(value_next, trainable_vars)

        # Lazily initialize when gradient shape known.
        if len(self._trace) == 0:
            for grad in grads:
                self._trace.append(tf.Variable(
                    tf.zeros(grad.get_shape()), trainable=False
                ))

        if player == 0 and board.won(player):
            reward = 1
        else:
            reward = 0

        td_error = tf.reduce_sum(reward + value_next - self._value)
        for i in range(len(grads)):
            self._trace[i].assign((self._LAMBDA * self._trace[i]) + grads[i])

            grad_trace = self._ALPHA * td_error * self._trace[i]
            self._model.trainable_variables[i].assign_add(grad_trace)

        self._state = tf.Variable(x_next)
        self._value = tf.Variable(value_next)

        duration = time.time() - start
        logging.debug("updating model [player = %d] [duration = %ds]", player, duration)

    def load(self, path):
        logging.info("loading checkpoint [path = %s]", path)

        ckpt = tf.train.Checkpoint(model=self._model, state=self._state, value=self._value)
        ckpt.restore(path)

    def save(self):
        if not os.path.exists('checkpoint'):
            os.mkdir('checkpoint')

        directory = 'checkpoint/model-' + str(datetime.datetime.now()).replace(' ', '_')
        if not os.path.exists(directory):
            os.mkdir(directory)

        ckpt = tf.train.Checkpoint(model=self._model, state=self._state, value=self._value)
        path = ckpt.save(directory)

        logging.info("saving checkpoint [path = %s]", path)

        return path

    def _reset_trace(self):
        for i in range(len(self._trace)):
            self._trace[i].assign(tf.zeros(self._trace[i].get_shape()))
