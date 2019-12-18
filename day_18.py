from collections import deque
from dataclasses import dataclass, field
from typing import List, Tuple, Set, Dict, FrozenSet


@dataclass(frozen=True)
class State:
    loc: Tuple[int, int]
    keys: FrozenSet[str]
    doors: FrozenSet[str]
    steps: int = 0
    collected: Tuple[str, ...] = ()

    def path_key(self):
        return self.loc, self.keys


class Board:
    def __init__(self, mat: List[str]):
        self.mat = mat

        loc = None
        self.keys = {}
        self.doors = {}
        self.walls = set()
        for r, row in enumerate(self.mat):
            for c, cell in enumerate(self.mat[r]):
                if cell == '@':
                    loc = (r, c)
                elif 'a' <= cell <= 'z':
                    self.keys[cell] = (r, c)
                elif 'A' <= cell <= 'Z':
                    self.doors[cell] = (r, c)
                elif cell == '#':
                    self.walls.add((r, c))

        self.initial_state = State(loc, frozenset(self.keys.keys()), frozenset(self.doors.keys()))

    def on_board(self, loc: Tuple[int, int]) -> bool:
        r, c = loc
        return 0 <= r < len(self.mat) and 0 <= c < len(self.mat[r])


def next_states(board: Board, state: State) -> List[State]:
    queue = deque([(state.loc, 0)])
    res = []
    seen = {state.loc}
    while len(queue) > 0:
        (r, c), steps = queue.popleft()
        for new_loc in [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]:
            char = board.mat[new_loc[0]][new_loc[1]]
            if board.on_board(new_loc) and \
                    new_loc not in seen and \
                    new_loc not in board.walls and \
                    (char not in board.doors or char not in state.doors):
                if char in board.keys and char in state.keys:
                    new_keys = state.keys - frozenset(char)
                    new_doors = state.doors - frozenset(char.upper())
                    new_collected = state.collected + (char,)
                    new_steps = state.steps + steps + 1
                    new_state = State(new_loc, new_keys, new_doors, new_steps, new_collected)
                    res.append(new_state)
                else:
                    queue.append((new_loc, steps + 1))

            seen.add(new_loc)
    return res


def shortest_path(board: Board) -> State:
    queue = deque([board.initial_state])
    seen = {}
    best = None

    while len(queue) > 0:
        state = queue.popleft()
        if seen.get(state.path_key(), 1e100) <= state.steps:
            continue
        else:
            seen[state.path_key()] = state.steps

        if len(state.keys) == 0:
            if best is None or state.steps < best.steps:
                best = state
        elif best is None or state.steps < best.steps:
            new_states = next_states(board, state)
            for s in new_states:
                queue.append(s)

    return best


def board_from_img(img: str) -> Board:
    return Board(img.strip().split('\n'))


def problem1():
    with open("day_18_input.txt") as f:
        img = f.read()

    board = board_from_img(img)
    return shortest_path(board)


if __name__ == '__main__':
    print(problem1())
