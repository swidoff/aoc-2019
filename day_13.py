from collections import Counter
from typing import List, Dict, Tuple

from day_11 import run_program_coroutine
from day_09 import program_in_file


def draw_tiles(program: List[int]) -> Dict[Tuple[int, int], int]:
    res = {}

    def draw_tiles():
        while True:
            x = (yield)
            y = (yield)
            tile = (yield)
            res[(x, y)] = tile

    draw_coroutine = draw_tiles()
    next(draw_coroutine)

    computer = run_program_coroutine(program, draw_coroutine)
    try:
        next(computer)
    except StopIteration:
        pass

    return res


def problem1():
    program = program_in_file('day_13_input.txt')
    tiles = draw_tiles(program)
    print(max(map(lambda x: x[0], tiles.keys())))
    print(max(map(lambda x: x[1], tiles.keys())))
    tile_counts = Counter(tiles.values())
    return tile_counts[2]


def play_game(program: List[int], rows=23, cols=44):
    program[0] = 2
    grid = [[' ' for _ in range(0, cols)] for _ in range(0, rows)]
    score = [0]

    ball_pos = [0, 0]
    paddle_pos = [0, 0]
    tile_map = [' ', '|', '#', '_', 'o']

    def draw_tiles():
        while True:
            x = (yield)
            y = (yield)
            tile_idx = (yield)
            if x == -1 and y == 0:
                score[0] = tile_idx
            else:
                tile = tile_map[tile_idx]
                grid[y][x] = tile
                if tile == 'o':
                    ball_pos[0] = x
                    ball_pos[1] = y
                elif tile == '_':
                    paddle_pos[0] = x
                    paddle_pos[1] = y

    draw_coroutine = draw_tiles()
    next(draw_coroutine)

    computer = run_program_coroutine(program, draw_coroutine)
    next(computer)

    def print_screen():
        print('\n'.join(''.join(row) for row in grid))

    def read_joystick():
        # print('(-1, 0, 1) >')
        # return int(input())
        if paddle_pos[0] < ball_pos[0]:
            return 1
        elif paddle_pos[0] > ball_pos[0]:
            return -1
        else:
            return 0

    try:
        while True:
            print_screen()
            inp = read_joystick()
            computer.send(inp)
    except StopIteration:
        pass

    print("Game over")
    print(score[0])
    return score[0]


def problem2():
    program = list(program_in_file('day_13_input.txt'))
    play_game(program)


if __name__ == '__main__':
    # print(problem1())
    print(problem2())
