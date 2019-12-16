import fileinput
from typing import Tuple, Iterator, List


def points_on_path_from_origin(path: List[str]) -> Iterator[Tuple[int, int]]:
    x = 0
    y = 0

    for p in path:
        dir = p[0]
        amount = int(p[1:])
        for i in range(1, amount + 1):
            if dir == 'R':
                x += 1
            elif dir == 'L':
                x -= 1
            elif dir == 'U':
                y += 1
            elif dir == 'D':
                y -= 1
            yield x, y


def steps_to_point(path: List[str], point: Tuple[int, int]) -> int:
    steps = 0
    for p in points_on_path_from_origin(path):
        steps += 1
        if p == point:
            break
    return steps


def path_intersections(path1: List[str], path2: List[str]) -> List[Tuple[int, int]]:
    points1 = set(points_on_path_from_origin(path1))
    return [p2 for p2 in points_on_path_from_origin(path2) if p2 in points1]


def manhattan_distance_to_origin(point: Tuple[int, int]):
    return sum(map(abs, point))


def shortest_distance_to_intersection_from_origin(path1: List[str], path2: List[str]):
    return min(map(manhattan_distance_to_origin, path_intersections(path1, path2)))


def shortest_steps_to_intersection_on_paths(path1: List[str], path2: List[str]) -> int:
    return min(
        steps_to_point(path1, point) + steps_to_point(path2, point)
        for point in path_intersections(path1, path2)
    )


def lines(file: str):
    with fileinput.input(files=(file,)) as f:
        for line in f:
            yield line.strip()


def problem1():
    ls = list(lines('day_03_input.txt'))
    path1 = ls[0].split(',')
    path2 = ls[1].split(',')
    return shortest_distance_to_intersection_from_origin(path1, path2)


def problem2():
    ls = list(lines('day_03_input.txt'))
    path1 = ls[0].split(',')
    path2 = ls[1].split(',')
    return shortest_steps_to_intersection_on_paths(path1, path2)


if __name__ == '__main__':
    print(problem1())
    print(problem2())
