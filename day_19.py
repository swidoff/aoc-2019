from collections import defaultdict
from typing import List, Tuple

from day_11 import run_program_coroutine, program_in_file


def is_point_in_beam(program: List[int], x: int, y: int) -> bool:
    output = []

    def record_output():
        while True:
            o = (yield)
            output.append(o)

    recorder = record_output()
    next(recorder)

    runner = run_program_coroutine(list(program), recorder)
    next(runner)

    try:
        runner.send(x)
        runner.send(y)
    except StopIteration:
        pass

    return output[-1] == 1


def map_beam(program: List[int], dim: int) -> str:
    mat = [
        [
            '#' if is_point_in_beam(program, x, y) else '.'
            for x in range(dim)
        ]
        for y in range(dim)
    ]
    return '\n'.join(''.join(c for c in row) for row in mat)


def problem1():
    program = list(program_in_file('day_19_input.txt'))
    beam = map_beam(program, 50)
    print(beam)
    return sum(1 if c == '#' else 0 for c in beam)


def find_square_in_beam(program, dim):
    x = 2
    y = 4
    coords = defaultdict(list)
    while not ((x - dim + 1) in coords and (coords[x][0] + dim - 1) in coords[x - dim + 1]):
        x += 1
        print(x)
        while not is_point_in_beam(program, x, y):
            y += 1

        coords[x].append(y)
        y += max(coords[x - 1][1] - coords[x - 1][0], 1) if len(coords) > 1 else 1
        while is_point_in_beam(program, x, y):
            y += 1

        coords[x].append(y - 1)
        y = coords[x][0]

    return x - dim + 1, coords[x][0]


def problem2():
    program = list(program_in_file('day_19_input.txt'))
    x, y = find_square_in_beam(program, 100)
    # 4: 26 35
    print(x, y)
    return x * 10000 + y


if __name__ == '__main__':
    # print(problem1())
    print(problem2())
