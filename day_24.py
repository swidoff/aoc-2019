from __future__ import annotations

from functools import reduce
from typing import List, Optional


class BugGrid(object):
    def __init__(self, n=5):
        self.n = n
        self.size = n * n
        self.masks = []

        mask = 1
        for i in range(self.size):
            self.masks.append(mask)
            mask <<= 1

    def mask_for(self, i: int):
        return self.masks[i] if 0 <= i < self.size else 0

    def bug_count(self, bits: int, i: int) -> int:
        return 1 if bits & self.mask_for(i) else 0

    def adjacent_bug_count(self, bits: int, i: int):
        rem = i % self.n
        return (self.bug_count(bits, i - 1) if rem > 0 else 0) + \
               (self.bug_count(bits, i + 1) if rem < self.n - 1 else 0) + \
               self.bug_count(bits, i - self.n) + \
               self.bug_count(bits, i + self.n)

    def step_i(self, bits: int, i: int) -> int:
        current = self.bug_count(bits, i)
        if current and self.adjacent_bug_count(bits, i) != 1:
            return 0
        elif not current and 1 <= self.adjacent_bug_count(bits, i) <= 2:
            return self.mask_for(i)
        else:
            return bits & self.mask_for(i)

    def step(self, bits: int) -> int:
        res = 0
        for i in range(self.size):
            mask = self.step_i(bits, i)
            if mask:
                res |= mask
        return res

    def first_repeated_bits(self, start: int, verbose: bool = False):
        seen = set()
        bits = start
        step = 0
        while bits not in seen:
            if verbose:
                print(f'Step: {step}')
                print(self.bits_to_str(bits))
                print()
            seen.add(bits)
            bits = self.step(bits)
            step += 1
        return bits

    def str_to_bits(self, mat: str) -> int:
        bits = 0
        grid = mat.split('\n')
        for r in range(self.n):
            for c in range(self.n):
                if grid[r][c] == '#':
                    bits |= self.masks[r * self.n + c]
        return bits

    def bits_to_str(self, bits: int) -> str:
        return "\n".join(
            "".join("#" if bits & self.masks[r * self.n + c] else "." for c in range(self.n))
            for r in range(self.n)
        )


def problem1():
    with open('day_24_input.txt') as f:
        start = f.read()

    grid = BugGrid(n=5)
    start_bits = grid.str_to_bits(start)
    return grid.first_repeated_bits(start_bits, verbose=False)


Grid = List[List[bool]]


def empty_grid() -> Grid:
    return [[False, False, False, False, False],
            [False, False, False, False, False],
            [False, False, False, False, False],
            [False, False, False, False, False],
            [False, False, False, False, False]]


def initial_grid(grid: str) -> Grid:
    return [list(c == "#" for c in line) for line in grid.split('\n')]


def grid_to_str(grid: Grid) -> str:
    return '\n'.join(''.join("#" if c else '.' for c in row) for row in grid)


def recursive_steps(grid: Grid, steps: int) -> List[Grid]:
    below = [empty_grid() for _ in range(steps // 2)]
    above = [empty_grid() for _ in range(steps // 2)]
    grids = below + [grid] + above
    return reduce(lambda g, _: recursive_step(g), range(steps), grids)


def recursive_step(grids: List[Grid]) -> List[Grid]:
    return [
        recursive_step_level(
            grids[i],
            above=grids[i - 1] if i > 0 else None,
            below=grids[i + 1] if i < len(grids) - 1 else None)
        for i in range(len(grids))
    ]


def recursive_count_bugs(grids: List[Grid]):
    count = 0
    for g in grids:
        for r in range(len(g)):
            for c in range(len(g[r])):
                count += g[r][c]
    return count


def recursive_step_level(grid: Grid, below: Optional[Grid] = None, above: Optional[Grid] = None) -> Grid:
    res = empty_grid()

    for r in range(5):
        for c in range(5):
            if r == 2 and c == 2:
                continue

            bug_count = recursive_adjacent_bugs(r, c, grid, below, above)

            val = grid[r][c]
            if val and bug_count != 1:
                new_val = 0
            elif not val and 1 <= bug_count <= 2:
                new_val = 1
            else:
                new_val = val

            res[r][c] = new_val

    return res


def recursive_adjacent_bugs(r: int, c: int, grid: Grid, below: Optional[Grid], above: Optional[Grid]) -> int:
    res = 0
    if above:
        if r == 0:
            res += above[1][2]
        elif r == 4:
            res += above[3][2]
        if c == 0:
            res += above[2][1]
        elif c == 4:
            res += above[2][3]
    if below:
        if r == 1 and c == 2:
            res += sum(below[0][i] for i in range(5))
        elif r == 2 and c == 1:
            res += sum(below[i][0] for i in range(5))
        elif r == 3 and c == 2:
            res += sum(below[4][i] for i in range(5))
        elif r == 2 and c == 3:
            res += sum(below[i][4] for i in range(5))

    if r - 1 >= 0:
        res += grid[r - 1][c]
    if r + 1 <= 4:
        res += grid[r + 1][c]
    if c - 1 >= 0:
        res += grid[r][c - 1]
    if c + 1 <= 4:
        res += grid[r][c + 1]

    return res


def problem2():
    with open('day_24_input.txt') as f:
        start = f.read()

    grid = initial_grid(start)
    final = recursive_steps(grid, 200)
    return recursive_count_bugs(final)


if __name__ == '__main__':
    # print(problem1())
    print(problem2())
