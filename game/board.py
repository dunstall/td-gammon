# Copyright 2021 Andrew Dunstall

import numpy as np


PLAYER_X = 0
PLAYER_O = 1


class Board:
    _NUM_POINTS = 24
    _STATE_SIZE = 198
    _NUM_CHECKERS = 15

    _MIN_MOVE = 1
    _MAX_MOVE = 6

    def __init__(self):
        self._x_points = np.array([
            0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0,
            5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2
        ])
        self._o_points = np.array([
            0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0,
            5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2
        ])
        self._x_bar = 0
        self._o_bar = 0
        self._x_removed = 0
        self._o_removed = 0

    def x_bar(self):
        return self._x_bar

    def o_bar(self):
        return self._o_bar

    def won(self, player):
        if player == PLAYER_X:
            return self._x_removed == self._NUM_CHECKERS
        if player == PLAYER_O:
            return self._o_removed == self._NUM_CHECKERS
        return False

    def x_points(self):
        return self._x_points

    def o_points(self):
        return self._o_points

    def permitted_moves(self, rolls, player=PLAYER_X):
        # Ensure rolls unique.
        rolls = list(set(rolls))

        permitted = []
        for steps in rolls:
            for position in range(24):
                if self._move_permitted(position, steps, player):
                    permitted.append((position, steps))
            if self._move_permitted("bar", steps, player):
                permitted.append(("bar", steps))

        return permitted

    def move(self, position, steps, player=PLAYER_X) -> bool:
        player_points = self._x_points if player == PLAYER_X else self._o_points
        opponent_points = self._o_points if player == PLAYER_X else self._x_points

        if not self._move_permitted(position, steps, player):
            return False

        if position == "bar":
            new_position = steps - 1
        else:
            new_position = position + steps

        # Bearing off.
        if new_position == self._NUM_POINTS:
            player_points[position] -= 1
            if player == PLAYER_X:
                self._x_removed += 1
            if player == PLAYER_O:
                self._o_removed += 1
            return True

        n_occupied = opponent_points[self._NUM_POINTS - new_position - 1]
        if n_occupied == 1:
            # Hit
            opponent_points[self._NUM_POINTS - new_position - 1] = 0
            if player == PLAYER_X:
                self._o_bar += 1
            else:
                self._x_bar += 1

        if position == "bar":
            player_points[new_position] += 1
            if player == PLAYER_X:
                self._x_bar -= 1
            if player == PLAYER_O:
                self._o_bar -= 1

        else:
            player_points[position] -= 1
            player_points[position + steps] += 1
        return True

    def state(self):
        return {
            "x_bar": self._x_bar,
            "o_bar": self._o_bar,
            "x_removed": self._x_removed,
            "o_removed": self._o_removed,
            "x_points": [int(n) for n in self._x_points],
            "o_points": [int(n) for n in self._o_points]
        }

    def encode_state(self, turn):
        state = np.zeros(self._STATE_SIZE)

        for point in range(self._NUM_POINTS):
            index = point * 4
            state[index:index+4] = encode_point(self._x_points[point])

        for point in range(self._NUM_POINTS):
            index = (point + 24) * 4
            state[index:index+4] = encode_point(self._o_points[point])

        state[192] = self._x_bar / 2
        state[193] = self._o_bar / 2
        state[194] = self._x_removed / self._NUM_CHECKERS
        state[195] = self._o_removed / self._NUM_CHECKERS
        state[196] = 1 - turn
        state[197] = turn

        return state

    def _move_permitted(self, position, steps, player) -> bool:
        player_points = self._x_points if player == PLAYER_X else self._o_points
        opponent_points = self._o_points if player == PLAYER_X else self._x_points

        if steps < self._MIN_MOVE or steps > self._MAX_MOVE:
            return False

        if position == "bar":
            if player == PLAYER_X and self._x_bar == 0:
                return False
            if player == PLAYER_O and self._o_bar == 0:
                return False

            new_position = steps - 1
            n_occupied = opponent_points[self._NUM_POINTS - new_position - 1]
            if n_occupied >= 2:
                return False

            return True

        if player == PLAYER_X and self._x_bar != 0:
            return False
        if player == PLAYER_O and self._o_bar != 0:
            return False

        # No checkers to move at this position.
        if player_points[position] == 0:
            return False

        new_position = position + steps
        # Note may be 24 if bearing off.
        if new_position > self._NUM_POINTS:
            return False

        if new_position == self._NUM_POINTS:
            return True

        # Point occupied by opponent.
        n_occupied = opponent_points[self._NUM_POINTS - new_position - 1]
        if n_occupied >= 2:
            return False

        return True


def encode_point(n_checkers):
    arr = np.zeros(4)
    if n_checkers == 1:  # Blot
        arr[0] = 1
    if n_checkers >= 2:  # Made point
        arr[1] = 1
    if n_checkers == 3:
        arr[2] = 1
    if n_checkers > 3:
        arr[3] = (n_checkers - 3) / 2
    return arr
