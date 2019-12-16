import math
from typing import Tuple, List

Vector = List[int]


def simulate_step(pos: List[Vector], vel: List[Vector]) -> Tuple[List[Vector], List[Vector]]:
    new_vel = [list(vel[i]) for i in range(len(vel))]
    for i in range(len(pos)):
        p1 = pos[i]
        for j in range(i + 1, len(pos)):
            p2 = pos[j]
            for k in range(0, 3):
                if p1[k] < p2[k]:
                    new_vel[i][k] += 1
                    new_vel[j][k] -= 1
                elif p1[k] > p2[k]:
                    new_vel[i][k] -= 1
                    new_vel[j][k] += 1

    new_pos = [list(pos[i]) for i in range(len(pos))]
    for i, (p, v) in enumerate(zip(pos, new_vel)):
        for k in range(0, 3):
            new_pos[i][k] = p[k] + v[k]

    return new_pos, new_vel


def simulate(initial_pos: List[Vector], steps: int) -> Tuple[List[Vector], List[Vector]]:
    pos = initial_pos
    vel = [[0, 0, 0] for i in range(len(initial_pos))]
    for i in range(0, steps):
        pos, vel = simulate_step(pos, vel)

    return pos, vel


def total_energy(pos: List[Vector], vel: List[Vector]) -> int:
    return sum(sum(map(abs, p)) * sum(map(abs, v)) for p, v in zip(pos, vel))


def problem1():
    pos, vel = simulate([
        [4, 1, 1],
        [11, -18, -1],
        [-2, -10, -4],
        [-7, -2, 14],
    ], 1000)
    return total_energy(pos, vel)


def simulate_step_1d(pos: List[Vector], vel: List[Vector], k: int) -> Tuple[List[Vector], List[Vector]]:
    new_vel = [list(vel[i]) for i in range(len(vel))]
    for i in range(len(pos)):
        p1 = pos[i]
        for j in range(i + 1, len(pos)):
            p2 = pos[j]
            if p1[k] < p2[k]:
                new_vel[i][k] += 1
                new_vel[j][k] -= 1
            elif p1[k] > p2[k]:
                new_vel[i][k] -= 1
                new_vel[j][k] += 1

    new_pos = [list(pos[i]) for i in range(len(pos))]
    for i, (p, v) in enumerate(zip(pos, new_vel)):
        new_pos[i][k] = p[k] + v[k]

    return new_pos, new_vel


def simulate_1d(initial_pos: List[Vector], steps: int) -> Tuple[List[Vector], List[Vector]]:
    pos = initial_pos
    vel = [[0, 0, 0] for i in range(len(initial_pos))]
    for i in range(0, steps):
        pos, vel = simulate_step_1d(pos, vel, 0)
        pos, vel = simulate_step_1d(pos, vel, 1)
        pos, vel = simulate_step_1d(pos, vel, 2)

    return pos, vel


def steps_until_repeat_1d(initial_pos: List[Vector], k: int) -> int:
    initial_vel = [[0, 0, 0] for i in range(len(initial_pos))]
    pos, vel = simulate_step_1d(initial_pos, initial_vel, k)
    steps = 1

    while (pos, vel) != (initial_pos, initial_vel):
        pos, vel = simulate_step_1d(pos, vel, k)
        steps += 1

    return steps


def lcm(num1, num2):
    return num1 * num2 // math.gcd(num1, num2)


def steps_until_repeat(initial_pos: List[Vector]) -> int:
    steps0 = steps_until_repeat_1d(initial_pos, 0)
    steps1 = steps_until_repeat_1d(initial_pos, 1)
    steps2 = steps_until_repeat_1d(initial_pos, 2)
    res = lcm(steps2, lcm(steps1, steps0))
    return res


def problem2():
    return steps_until_repeat([
        [4, 1, 1],
        [11, -18, -1],
        [-2, -10, -4],
        [-7, -2, 14],
    ])


if __name__ == '__main__':
    print(problem1())
    print(problem2())
