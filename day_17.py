from collections import deque
from enum import Enum
from typing import List, Tuple

from more_itertools import flatten

from day_11 import run_program_coroutine, program_in_file


def draw_map(program: List[int]) -> str:
    output = []

    def record_output():
        while True:
            o = (yield)
            output.append(chr(o))

    recorder = record_output()
    next(recorder)

    runner = run_program_coroutine(program, recorder)
    try:
        next(runner)
    except StopIteration:
        pass

    return "".join(output[:-2])


def locate_intersections(img: str):
    mat = img.split('\n')

    return [
        (r, c)
        for r in range(1, len(mat) - 2)
        for c in range(1, len(mat[r]) - 2)
        if mat[r][c] == '#'
           and mat[r - 1][c] == '#'
           and mat[r + 1][c] == '#'
           and mat[r][c - 1] == '#'
           and mat[r][c + 1] == '#'
    ]


def problem1():
    program = list(program_in_file('day_17_input.txt'))
    img = draw_map(program)
    intersections = locate_intersections(img)
    return sum(r * c for r, c in intersections)


class Direction(Enum):
    UP = 0
    LEFT = 1
    DOWN = 2
    RIGHT = 3

    def rotate_left(self):
        return Direction((self.value + 1) % 4)

    def rotate_right(self):
        new_val = self.value - 1
        return Direction(new_val if new_val >= 0 else 3)

    def move(self, coord: Tuple[int, int]) -> Tuple[int, int]:
        if self == Direction.UP:
            return coord[0] - 1, coord[1]
        elif self == Direction.DOWN:
            return coord[0] + 1, coord[1]
        elif self == Direction.RIGHT:
            return coord[0], coord[1] + 1
        else:
            return coord[0], coord[1] - 1

    def icon(self):
        if self == Direction.UP:
            return "^"
        elif self == Direction.DOWN:
            return "v"
        elif self == Direction.RIGHT:
            return ">"
        else:
            return "<"


def cover_scaffolds(img: str) -> List[str]:
    mat = img.split('\n')
    scaffolds, coord = find_scaffolds_and_robot(mat)
    remaining = set(scaffolds)

    path = []
    direction = Direction.UP
    print(print_map(img, remaining, coord, direction))

    while len(remaining) > 0:
        if direction.move(coord) in scaffolds:
            coord = direction.move(coord)
            if coord in remaining:
                remaining.remove(coord)
            path.append('1')
        elif direction.rotate_left().move(coord) in scaffolds:
            direction = direction.rotate_left()
            path.append('L')
        elif direction.rotate_right().move(coord) in scaffolds:
            direction = direction.rotate_right()
            path.append('R')
        else:
            raise ValueError("Backtracking required!")
        print(print_map(img, remaining, coord, direction))
    return path


def find_scaffolds_and_robot(mat):
    res = set()
    coord = None
    for r in range(len(mat)):
        for c in range(len(mat[r])):
            if mat[r][c] == '#':
                res.add((r, c))
            elif mat[r][c] == '^':
                coord = (r, c)
    return res, coord


def print_map(img, remaining, robot_coord, direction):
    mat = img.split('\n')

    def map_gen():
        for r in range(len(mat)):
            for c in range(len(mat[r])):
                if (r, c) == robot_coord:
                    yield direction.icon()
                elif mat[r][c] == '#' and (r, c) not in remaining:
                    yield '*'
                elif mat[r][c] == '^':
                    yield '*'
                else:
                    yield mat[r][c]
            yield "\n"

    return "".join(map_gen())


def condense_path(path: List[str]):
    count = 0
    for c in path:
        if c == 'L' or c == 'R':
            if count > 0:
                yield str(count)
                count = 0
            yield c
        else:
            count += 1

    if count > 0:
        yield count


def move_robot(program: List[int], main: str, functions: List[str]) -> int:
    output = []
    last = [0]
    program[0] = 2

    def record_output():
        while True:
            o = (yield)
            if chr(o) == '\n':
                print(''.join(output))
                output.clear()
            else:
                output.append(chr(o))
                last[0] = o

    recorder = record_output()
    next(recorder)

    runner = run_program_coroutine(program, recorder)
    next(runner)

    def send_code(line):
        for c in line:
            runner.send(ord(c))
        runner.send(10)

    try:
        send_code(main)
        for f in functions:
            send_code(f)
        send_code('n')
    except StopIteration:
        pass

    return last[0]


def problem2_part1():
    program = list(program_in_file('day_17_input.txt'))
    img = draw_map(program)
    path = list(condense_path(cover_scaffolds(img)))
    return path


def problem2_part2():
    """
    Optimal path:
    A: 'L', '6', 'R', '8', 'L', '4', 'R', '8', 'L', '12',
    B: 'L', '12', 'R', '10', 'L', '4',
    B: 'L', '12', 'R', '10', 'L', '4',
    C: 'L', '12', 'L', '6', 'L', '4', 'L', '4',
    B: 'L', '12', 'R', '10', 'L', '4',
    C:'L', '12', 'L', '6', 'L', '4', 'L', '4',
    B: 'L', '12', 'R', '10', 'L', '4',
    C: 'L', '12', 'L', '6', 'L', '4', 'L', '4',
    A: 'L', '6', 'R', '8', 'L', '4', 'R', '8', 'L', '12',
    A: 'L', '6', 'R', '8', 'L', '4', 'R', '8', 'L', '12'
    """
    program = list(program_in_file('day_17_input.txt'))
    main = 'A,B,B,C,B,C,B,C,A,A'
    functions = [
        'L,6,R,8,L,4,R,8,L,12',
        'L,12,R,10,L,4',
        'L,12,L,6,L,4,L,4'
    ]
    return move_robot(program, main, functions)


if __name__ == '__main__':
    # print(problem1())
    # print(draw_map(list(program_in_file('day_17_input.txt'))))
    img1 = """
..#..........
..#..........
#######...###
#.#...#...#.#
#############
..#...#...#..
..#####...^..
"""

    img2 = """
#######...#####
#.....#...#...#
#.....#...#...#
......#...#...#
......#...###.#
......#.....#.#
^########...#.#
......#.#...#.#
......#########
........#...#..
....#########..
....#...#......
....#...#......
....#...#......
....#####......
"""
    # print(cover_scaffolds(img1.strip()))
    # print(list(condense_path(cover_scaffolds(img2.strip()))))
    # print(problem2_part1())
    print(problem2_part2())
