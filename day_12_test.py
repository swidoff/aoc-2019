from day_12 import *


def test_simulate():
    pos, vel = simulate([
        [-1, 0, 2],
        [2, -10, -7],
        [4, -8, 8],
        [3, 5, -1],
    ], 10)
    assert (total_energy(pos, vel) == 179)

    pos, vel = simulate([
        [-8, -10, 0],
        [5, 5, 10],
        [2, -7, 3],
        [9, -8, -3],
    ], 100)
    assert (total_energy(pos, vel) == 1940)


def test_simulate_1d():
    pos, vel = simulate_1d([
        [-1, 0, 2],
        [2, -10, -7],
        [4, -8, 8],
        [3, 5, -1],
    ], 10)
    assert (total_energy(pos, vel) == 179)

    pos, vel = simulate_1d([
        [-8, -10, 0],
        [5, 5, 10],
        [2, -7, 3],
        [9, -8, -3],
    ], 100)
    assert (total_energy(pos, vel) == 1940)


def test_steps_until_repeat():
    assert (steps_until_repeat([
        [-1, 0, 2],
        [2, -10, -7],
        [4, -8, 8],
        [3, 5, -1],
    ]) == 2772)

    assert (steps_until_repeat([
        [-8, -10, 0],
        [5, 5, 10],
        [2, -7, 3],
        [9, -8, -3],
    ]) == 4686774924)
