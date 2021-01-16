# Copyright 2021 Andrew Dunstall

import unittest

import numpy as np

from game import board


class TestBoard(unittest.TestCase):
    # TODO(AD) Test with different player

    def test_move_from_bar_ok(self):
        b = board.Board()
        b._x_points[5] -= 1
        b._x_bar += 1
        self.assertTrue(b.move("bar", 2))
        self.assertEqual(0, b.x_bar())
        self.assertEqual(1, b.x_points()[1])

    def test_move_from_bar_blocked(self):
        b = board.Board()
        b._x_points[5] -= 1
        b._x_bar += 1
        state = b.state()
        self.assertFalse(b.move("bar", 1))
        self.assertEqual(state, b.state())

    def test_permitted_moves_one_step(self):
        b = board.Board()
        self.assertEqual([(5, 1), (7, 1), (12, 1), (23, 1)], b.permitted_moves([1, 1]))

    def test_permitted_moves_blocked(self):
        b = board.Board()
        self.assertEqual([(5, 4), (7, 6)], b.permitted_moves([4, 6]))

    def test_move_ok(self):
        b = board.Board()
        self.assertTrue(b.move(5, 2))
        self.assertEqual(4, b.x_points()[5])
        self.assertEqual(4, b.x_points()[7])

    def test_hit(self):
        b = board.Board()
        b._o_points[7] = 1
        self.assertTrue(b.move(12, 4))
        self.assertEqual(0, b.o_points()[7])
        self.assertEqual(1, b.o_bar())

    def test_move_bar_not_empty(self):
        b = board.Board()
        b._x_points[5] -= 1
        b._x_bar += 1
        state = b.state()
        self.assertFalse(b.move(5, 2))
        self.assertEqual(state, b.state())

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

    def test_encode_state_initial_state_x_turn(self):
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

    def test_encode_state_initial_state_o_turn(self):
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
