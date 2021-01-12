# Copyright 2021 Andrew Dunstall

import numpy as np


PLAYER_WHITE = 0
PLAYER_BLACK = 1


# TODO(AD) Properly unittest and rewrite this
class Board:
    _NUM_POINTS = 24
    _STATE_SIZE = 198

    _MIN_MOVE = 1
    _MAX_MOVE = 6

    def __init__(self):
        self._whites = np.array([
            0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0,
            5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2
        ])
        self._blacks = np.array([
            0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0,
            5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2
        ])
        self._white_bar = 0
        self._black_bar = 0
        self._white_removed = 0
        self._black_removed = 0

    def white_bar(self):
        return self._white_bar

    def black_bar(self):
        return self._black_bar

    def white_won(self):
        return self._white_removed == 15

    def black_won(self):
        return self._black_removed == 15

    # TODO(AD) properties
    def whites(self):
        return self._whites

    def blacks(self):
        return self._blacks

    def permitted_moves(self, rolls, player=PLAYER_WHITE):
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

    # TODO(AD) Bearing off - if new_position == 24
    def move(self, position, steps, player=PLAYER_WHITE) -> bool:
        player_points = self._whites if player == PLAYER_WHITE else self._blacks
        opponent_points = self._blacks if player == PLAYER_WHITE else self._whites

        if not self._move_permitted(position, steps, player):
            return False

        if position == "bar":
            new_position = steps - 1
        else:
            new_position = position + steps

        # Bearing off.
        if new_position == self._NUM_POINTS:
            #  print("bearing off")
            player_points[position] -= 1
            if player == PLAYER_WHITE:
                self._white_removed += 1
            if player == PLAYER_BLACK:
                self._black_removed += 1
            return True

        n_occupied = opponent_points[self._NUM_POINTS - new_position - 1]
        if n_occupied == 1:
            # Hit
            opponent_points[self._NUM_POINTS - new_position - 1] = 0
            if player == PLAYER_WHITE:
                 self._black_bar += 1
            else:
                 self._white_bar += 1

        if position == "bar":
            player_points[new_position] += 1
            if player == PLAYER_WHITE:
                self._white_bar -= 1
            if player == PLAYER_BLACK:
                self._black_bar -= 1

        else:
            player_points[position] -= 1
            player_points[position + steps] += 1
        return True

    def state(self):
        return {
            "white_bar": self._white_bar,
            "black_bar": self._black_bar,
            "white_removed": self._white_removed,
            "black_removed": self._black_removed,
            "white": [int(n) for n in self._whites],
            "black": [int(n) for n in self._blacks]
        }

    def encode_state(self, turn):
        state = np.zeros(self._STATE_SIZE)

        for point in range(self._NUM_POINTS):
            index = point * 4
            state[index:index+4] = encode_point(self._whites[point])

        for point in range(self._NUM_POINTS):
            index = (point + 24) * 4
            state[index:index+4] = encode_point(self._blacks[point])

        state[192] = self._white_bar / 2
        state[193] = self._black_bar / 2
        state[194] = self._white_removed / 15
        state[195] = self._black_removed / 15
        state[196] = 1 - turn
        state[197] = turn

        return state

    def _move_permitted(self, position, steps, player) -> bool:
        player_points = self._whites if player == PLAYER_WHITE else self._blacks
        opponent_points = self._blacks if player == PLAYER_WHITE else self._whites

        if steps < self._MIN_MOVE or steps > self._MAX_MOVE:
            return False

        if position == "bar":
            if player == PLAYER_WHITE and self._white_bar == 0:
                return False
            if player == PLAYER_BLACK and self._black_bar == 0:
                return False

            new_position = steps - 1
            n_occupied = opponent_points[self._NUM_POINTS - new_position - 1]
            if n_occupied >= 2:
                return False

            return True

        if player == PLAYER_WHITE and self._white_bar != 0:
            return False
        if player == PLAYER_BLACK and self._black_bar != 0:
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
