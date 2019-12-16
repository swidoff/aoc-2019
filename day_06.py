import fileinput
from itertools import takewhile
from typing import Dict, List


def total_orbits_for(b: str, orbits: Dict[str, str]):
    res = 0
    current = b
    while current in orbits:
        res += 1
        current = orbits[current]
    return res


def total_orbits(orbits: Dict[str, str]) -> int:
    return sum(total_orbits_for(b, orbits) for b in orbits)


def orbits_from_file(file: str) -> Dict[str, str]:
    res = {}
    with fileinput.input(files=(file,)) as f:
        for line in f:
            parts = line.strip().split(')')
            res[parts[1]] = parts[0]
    return res


def path_to_com(orbits: Dict[str, str], start: str) -> List[str]:
    res = []
    current = start
    while current in orbits:
        current = orbits[current]
        res.append(current)
    return res


def common_ancestor(path1: List[str], path2: List[str]):
    path1_components = dict(zip(path1, range(0, len(path1))))
    min_index = len(path1)
    min_node = ""
    for c in path2:
        if c in path1_components and path1_components[c] < min_index:
            min_node = c
            min_index = path1_components[c]
    return min_node


def path_steps(path: List[str], end: str):
    return sum(map(lambda _: 1, takewhile(lambda c: c != end, path)))


def min_transfers(orbits: Dict[str, str], start: str, end: str):
    path1 = path_to_com(orbits, start)
    path2 = path_to_com(orbits, end)
    ancestor = common_ancestor(path1, path2)
    return path_steps(path1, ancestor) + path_steps(path2, ancestor)


def problem1() -> int:
    orbits = orbits_from_file('day_06_input.txt')
    return total_orbits(orbits)


def problem2() -> int:
    orbits = orbits_from_file('day_06_input.txt')
    return min_transfers(orbits, 'YOU', 'SAN')


if __name__ == '__main__':
    print(problem1())
    print(problem2())
