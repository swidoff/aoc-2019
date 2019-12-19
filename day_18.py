from collections import deque, defaultdict, namedtuple
from dataclasses import dataclass, field
from typing import List, Tuple, Set, Dict, FrozenSet
import heapq


class Board:
    def __init__(self, mat: List[str]):
        self.mat = mat

        start = []
        self.keys = {}
        self.doors = {}
        self.walls = set()
        for r, row in enumerate(self.mat):
            for c, cell in enumerate(self.mat[r]):
                if cell == '@':
                    start.append((r, c))
                elif 'a' <= cell <= 'z':
                    self.keys[cell] = (r, c)
                elif 'A' <= cell <= 'Z':
                    self.doors[cell] = (r, c)
                elif cell == '#':
                    self.walls.add((r, c))

        self.start = tuple(start)

    def on_board(self, loc: Tuple[int, int]) -> bool:
        r, c = loc
        return 0 <= r < len(self.mat) and 0 <= c < len(self.mat[r])


@dataclass(frozen=True)
class Edge(object):
    key: str
    doors: FrozenSet[str] = frozenset()
    steps: int = 0


def to_graphs(board: Board) -> List[Dict[str, List[Edge]]]:
    def to_graph_from(start: str, loc: Tuple[int, int]):
        res = defaultdict(list)
        queue = deque([(start, loc, (), 0)])
        seen = set()
        while len(queue) > 0:
            sym, loc, doors, steps = queue.popleft()
            seen.add((sym, loc))

            r, c = loc
            for new_loc in [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]:
                if (sym, new_loc) in seen or not board.on_board(new_loc):
                    continue

                new_sym = board.mat[new_loc[0]][new_loc[1]]
                if new_sym == '#':
                    continue
                elif sym != new_sym and (new_sym in board.keys):
                    res[sym].append(Edge(new_sym, frozenset(doors), steps + 1))

                    if new_sym not in res:
                        queue.append((new_sym, new_loc, (), 0))
                elif new_sym in board.doors:
                    new_doors = doors + (new_sym,)
                    queue.append((sym, new_loc, new_doors, steps + 1))
                else:
                    queue.append((sym, new_loc, doors, steps + 1))

        return res

    return [to_graph_from('@', board.start[i]) for i in range(len(board.start))]


State = namedtuple("State", ["steps", "robots", "collected"])


def shortest_path(board: Board) -> State:
    graphs = to_graphs(board)
    initial_state = State(0, tuple(['@'] * len(board.start)), frozenset())
    queue = []
    heapq.heappush(queue, initial_state)

    seen = {}
    best = None

    while len(queue) > 0:
        state = heapq.heappop(queue)
        key = (state.robots, state.collected)
        if seen.get(key, 1e100) > state.steps:
            seen[key] = state.steps

            if len(state.collected) == len(board.keys):
                if best is None or state.steps < best.steps:
                    best = state
            elif best is None or state.steps < best.steps:
                for i, node in enumerate(state.robots):
                    for edge in graphs[i][node]:
                        if all(d.lower() in state.collected for d in edge.doors):
                            new_robots = state.robots[:i] + (edge.key,) + state.robots[i + 1:]
                            new_collected = state.collected | {edge.key}
                            new_steps = state.steps + edge.steps
                            new_state = State(new_steps, new_robots, new_collected)
                            heapq.heappush(queue, new_state)

    return best


def board_from_img(img: str) -> Board:
    return Board(img.strip().split('\n'))


def problem1():
    with open("day_18_input.txt") as f:
        img = f.read()

    board = board_from_img(img)
    return shortest_path(board)


def problem2():
    with open("day_18_input.txt") as f:
        img = f.read()

    initial_board = board_from_img(img)

    r, c = initial_board.start[0]
    mat = initial_board.mat
    mat = [[c for c in row] for row in mat]
    mat[r - 1][c - 1] = "@"
    mat[r - 1][c] = "#"
    mat[r - 1][c + 1] = "@"
    mat[r][c - 1] = "#"
    mat[r][c] = "#"
    mat[r][c + 1] = "#"
    mat[r + 1][c - 1] = "@"
    mat[r + 1][c] = "#"
    mat[r + 1][c + 1] = "@"

    img2 = "\n".join("".join(row) for row in mat)
    board = board_from_img(img2)
    return shortest_path(board)


if __name__ == '__main__':
    print(problem1())
    print(problem2())
