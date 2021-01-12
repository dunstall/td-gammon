# Copyright 2021 Andrew Dunstall

import abc


class Player(abc.ABC):
    @abc.abstractmethod
    async def turn(self, board):
        pass
