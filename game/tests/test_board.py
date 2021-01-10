# Copyright 2021 Andrew Dunstall

import unittest

import numpy as np

from game import board


class TestBoard(unittest.TestCase):
    def test_move_ok(self):
        b = board.Board()
        self.assertTrue(b.move(5, 2))
        self.assertEqual(4, b.whites()[5])
        self.assertEqual(4, b.whites()[7])

    def test_hit(self):
        b = board.Board()
        b._blacks[7] = 1
        self.assertTrue(b.move(12, 4))
        self.assertEqual(0, b.blacks()[7])
        self.assertEqual(1, b.black_bar())

    def test_move_to_occupied_point(self):
        b = board.Board()
        state = b.state()
        self.assertFalse(b.move(7, 4))
        self.assertEqual(state, b.state())

    def test_move_out_of_bounds(self):
        b = board.Board()
        state = b.state()
        self.assertFalse(b.move(23, 2))
        self.assertEqual(state, b.state())

    def test_move_point_empty(self):
        b = board.Board()
        state = b.state()
        self.assertFalse(b.move(0, 3))
        self.assertEqual(state, b.state())

    def test_move_step_too_large(self):
        b = board.Board()
        state = b.state()
        self.assertFalse(b.move(5, 7))
        self.assertEqual(state, b.state())

    def test_move_step_too_small(self):
        b = board.Board()
        state = b.state()
        self.assertFalse(b.move(5, 0))
        self.assertEqual(state, b.state())

    def test_encode_state_initial_state_white_turn(self):
        b = board.Board()
        state = b.encode_state(0)

        expected = np.array([
            0.0, 0.0, 0.0, 0.0,            0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0,            0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0,            0.0, 1.0, 0.0, 1.0,
            0.0, 0.0, 0.0, 0.0,            0.0, 1.0, 1.0, 0.0,
            0.0, 0.0, 0.0, 0.0,            0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0,            0.0, 0.0, 0.0, 0.0,
            0.0, 1.0, 0.0, 1.0,            0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0,            0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0,            0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0,            0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0,            0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0,            0.0, 1.0, 0.0, 0.0,

            0.0, 0.0, 0.0, 0.0,            0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0,            0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0,            0.0, 1.0, 0.0, 1.0,
            0.0, 0.0, 0.0, 0.0,            0.0, 1.0, 1.0, 0.0,
            0.0, 0.0, 0.0, 0.0,            0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0,            0.0, 0.0, 0.0, 0.0,
            0.0, 1.0, 0.0, 1.0,            0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0,            0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0,            0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0,            0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0,            0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0,            0.0, 1.0, 0.0, 0.0,

            0.0, 0.0,
            0.0, 0.0,
            1.0, 0.0
        ])

        self.assertTrue((expected == state).all())

    def test_encode_state_initial_state_black_turn(self):
        b = board.Board()
        state = b.encode_state(1)

        expected = np.array([
            0.0, 0.0, 0.0, 0.0,            0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0,            0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0,            0.0, 1.0, 0.0, 1.0,
            0.0, 0.0, 0.0, 0.0,            0.0, 1.0, 1.0, 0.0,
            0.0, 0.0, 0.0, 0.0,            0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0,            0.0, 0.0, 0.0, 0.0,
            0.0, 1.0, 0.0, 1.0,            0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0,            0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0,            0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0,            0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0,            0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0,            0.0, 1.0, 0.0, 0.0,

            0.0, 0.0, 0.0, 0.0,            0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0,            0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0,            0.0, 1.0, 0.0, 1.0,
            0.0, 0.0, 0.0, 0.0,            0.0, 1.0, 1.0, 0.0,
            0.0, 0.0, 0.0, 0.0,            0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0,            0.0, 0.0, 0.0, 0.0,
            0.0, 1.0, 0.0, 1.0,            0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0,            0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0,            0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0,            0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0,            0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0,            0.0, 1.0, 0.0, 0.0,

            0.0, 0.0,
            0.0, 0.0,
            0.0, 1.0
        ])

        self.assertTrue((expected == state).all())

    def test_encode_point_empty(self):
        self.assertTrue((np.zeros(4) == board.encode_point(0)).all())

    def test_encode_point_blot(self):
        self.assertTrue((np.array([1, 0, 0, 0]) == board.encode_point(1)).all())

    def test_encode_point_made_point(self):
        self.assertTrue((np.array([0, 1, 0, 0]) == board.encode_point(2)).all())

    def test_encode_point_3(self):
        self.assertTrue((np.array([0, 1, 1, 0]) == board.encode_point(3)).all())

    def test_encode_point_4(self):
        self.assertTrue((np.array([0, 1, 0, 0.5]) == board.encode_point(4)).all())

    def test_encode_point_5(self):
        self.assertTrue((np.array([0, 1, 0, 1]) == board.encode_point(5)).all())
