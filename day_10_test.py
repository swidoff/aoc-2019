from io import StringIO

from day_10 import *


def test_points_on_line():
    print(points_on_segment(0, 0, 9, 3))


def test_count_detections():
    mstr = """
.#..#
.....
#####
....#
...##
"""
    m = matrix_in_file(StringIO(mstr))
    assert (count_detections(m, 1, 0) == 7)
    assert (count_detections(m, 4, 0) == 7)
    assert (count_detections(m, 0, 2) == 6)
    assert (count_detections(m, 1, 2) == 7)
    assert (count_detections(m, 2, 2) == 7)
    assert (count_detections(m, 3, 2) == 7)
    assert (count_detections(m, 4, 2) == 5)
    assert (count_detections(m, 4, 3) == 7)
    assert (count_detections(m, 3, 4) == 8)
    assert (count_detections(m, 4, 4) == 7)


def test_best_asteroid():
    mstr = """
......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####
"""
    assert (best_asteroid(matrix_in_file(StringIO(mstr))) == (33, 5, 8))

    mstr = """
#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.
"""
    assert (best_asteroid(matrix_in_file(StringIO(mstr))) == (35, 1, 2))

    mstr = """
.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..
"""
    assert (best_asteroid(matrix_in_file(StringIO(mstr))) == (41, 6, 3))

    mstr = """
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
"""
    assert (best_asteroid(matrix_in_file(StringIO(mstr))) == (210, 11, 13))


def test_vaporize():
    mstr = """
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
"""
    m = matrix_in_file(StringIO(mstr))
    # print(is_obstructed(m, 11, 13, 11, 10))
    res = vaporize(m, 11, 13)
    print(res[1-1])
    print(res[2-1])
    print(res[3-1])
    print(res[10-1])
    print(res[20-1])
    print(res[50-1])
    print(res[100-1])
    print(res[199-1])
    print(res[200-1])
