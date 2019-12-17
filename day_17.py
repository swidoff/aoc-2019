from collections import deque
from enum import Enum
from typing import List, Tuple

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
    remaining, coord = find_scaffolds_and_robot(mat)

    path = []
    stack = deque()
    direction = Direction.UP
    backtracking = False
    print(print_map(img, remaining, coord, direction))

    while len(remaining) > 0:
        if direction.move(coord) in remaining:
            new_coord = direction.move(coord)
            path.append('1')
            stack.append(coord)
            coord = new_coord
            remaining.remove(new_coord)
            backtracking = False
        elif direction.rotate_left().move(coord) in remaining:
            direction = direction.rotate_left()
            path.append('L')
            stack.append(coord)
            backtracking = False
        elif direction.rotate_right().move(coord) in remaining:
            direction = direction.rotate_right()
            path.append('R')
            stack.append(coord)
            backtracking = False
        else:
            if not backtracking:
                direction = direction.rotate_left().rotate_left()
                path.extend(['L', 'L'])
                backtracking = True
            new_coord = stack.pop()
            if direction.move(coord) == new_coord:
                path.append('1')
            elif direction.rotate_right().move(coord) == new_coord:
                path.append('R')
                direction = direction.rotate_right()
            else:
                path.append('L')
                direction = direction.rotate_left()
            coord = new_coord
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


def print_map(img, scaffolds, robot_coord, direction):
    mat = img.split('\n')

    def map_gen():
        for r in range(len(mat)):
            for c in range(len(mat[r])):
                if (r, c) == robot_coord:
                    yield direction.icon()
                elif mat[r][c] == '#' and (r, c) not in scaffolds:
                    yield '*'
                elif mat[r][c] == '^':
                    yield '*'
                else:
                    yield mat[r][c]
            yield "\n"

    return "".join(map_gen())


def problem2():
    program = list(program_in_file('day_17_input.txt'))
    img = draw_map(program)
    path = cover_scaffolds(img)
    # program[0] = 2
    return path


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
    # print(cover_scaffolds(img2.strip()))
    print(problem2())
