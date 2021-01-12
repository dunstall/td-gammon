# Copyright 2021 Andrew Dunstall

import abc
import random


class Player(abc.ABC):
    @abc.abstractmethod
    async def turn(self, board):
        pass

    def _roll(self):
        roll1 = random.randint(1, 6)
        roll2 = random.randint(1, 6)
        if roll1 == roll2:
            # Doubles.
            self._rolls = [roll1] * 4
        else:
            self._rolls = [roll1, roll2]
