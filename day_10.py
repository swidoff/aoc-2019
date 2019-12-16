import math
from collections import defaultdict
from io import StringIO
from typing import List, Tuple


def points_on_segment(x1: int, y1: int, x2: int, y2: int) -> List[Tuple[int, int]]:
    slope_y = y2 - y1
    slope_x = x2 - x1
    if slope_x == 0:
        slope_y = 1 if slope_y > 0 else -1
    elif slope_y == 0:
        slope_x = 1 if slope_x > 0 else -1
    else:
        gcd = math.gcd(abs(slope_y), abs(slope_x))
        slope_y //= gcd
        slope_x //= gcd

    point_x = x1 + slope_x
    point_y = y1 + slope_y
    res = []
    while not (point_x == x2 and point_y == y2):
        res.append((point_x, point_y))
        point_x += slope_x
        point_y += slope_y
    return res


def count_obstructions(m: List[List[bool]], x1: int, y1: int, x2: int, y2: int) -> int:
    points = points_on_segment(x1, y1, x2, y2)
    return sum(m[y][x] for x, y in points) if points else 0


def is_obstructed(m: List[List[bool]], x1: int, y1: int, x2: int, y2: int) -> bool:
    return count_obstructions(m, x1, y1, x2, y2) > 0


def count_detections(m: List[List[bool]], origin_x: int, origin_y: int) -> int:
    count = 0
    for y in range(0, len(m)):
        for x in range(0, len(m[y])):
            if m[y][x] and (x, y) != (origin_x, origin_y) and not is_obstructed(m, origin_x, origin_y, x, y):
                count += 1
    return count


def best_asteroid(m: List[List[bool]]) -> Tuple[int, int, int]:
    best_x = -1
    best_y = -1
    best_count = -1
    for y in range(0, len(m)):
        for x in range(0, len(m[y])):
            if m[y][x]:
                count = count_detections(m, x, y)
                if count > best_count:
                    best_x = x
                    best_y = y
                    best_count = count
    return best_count, best_x, best_y


def matrix_in_file(file) -> List[List[bool]]:
    res = []

    f = open(file) if not isinstance(file, StringIO) else file

    line = f.readline()
    while line:
        if len(line.strip()) > 0:
            row = []
            for c in line.strip():
                row.append(False if c == '.' else True)
            res.append(row)
        line = f.readline()

    f.close()
    return res


def problem1():
    m = matrix_in_file('day_10_input.txt')
    return best_asteroid(m)


def angle(x1: int, y1: int, x2: int, y2: int) -> float:
    opposite = x2 - x1
    adjacent = y1 - y2
    if adjacent == 0:
        return 90. if opposite > 0 else 180.
    else:
        res = math.degrees(math.atan2(abs(opposite), abs(adjacent)))
        if adjacent < 0 and opposite >= 0:
            res = 180 - res
        elif adjacent < 0 and opposite < 0:
            res = 270 - res
        elif adjacent > 0 and opposite < 0:
            res = 360 - res
        return res


def vaporize(m: List[List[bool]], origin_x: int, origin_y: int) -> List[Tuple[int, int]]:
    points = []
    for y in range(0, len(m)):
        for x in range(0, len(m[y])):
            if m[y][x] and (x, y) != (origin_x, origin_y):
                points.append((x, y))

    res = []
    points = sorted(points, key=lambda p: angle(origin_x, origin_y, p[0], p[1]))
    while len(points) > 0:
        to_remove = []
        for x, y in points:
            if not is_obstructed(m, origin_x, origin_y, x, y):
                res.append((x, y))
                to_remove.append((x, y))

        for x, y in to_remove:
            points.remove((x, y))
            m[y][x] = False
    return res


def problem2():
    m = matrix_in_file('day_10_input.txt')
    return vaporize(m, 17, 22)


if __name__ == '__main__':
    print(problem1())
    print(problem2()[199])
