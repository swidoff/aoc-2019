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


def find_square_in_beam(program, dim) -> Tuple[int, int]:
    """
    Returns the x,y coordinates of the upper left corner of the dim x dim square contained entirely in the
    beam that has the lowest x value (closest to the emitter at x=0).

    Could use a binary search to locate the x coord rather than a linear search. We kind of know the slope
    of the upper vector of the beam, so could use that to pick a reasonable place to start looking for y.
    """
    x = 3
    y = 4

    # Continue until the lower left corner of the square is in the beam where the upper right corner is the
    # min y of the last x value.
    while not is_point_in_beam(program, x - dim + 1, y + dim - 1):
        # Start scanning at the first y of prior x for the start of the beam, since the
        # beam is pointing "downward" (toward greater y values) the y start will never decrease.
        x += 1
        while not is_point_in_beam(program, x, y):
            y += 1

    # Return the upper left corner of the square.
    return x - dim + 1, y


def problem2():
    program = list(program_in_file('day_19_input.txt'))
    x, y = find_square_in_beam(program, 100)
    # 4: 27 35
    # 100: 838 1082
    print(x, y)
    return x * 10000 + y


if __name__ == '__main__':
    # print(problem1())
    print(problem2())
