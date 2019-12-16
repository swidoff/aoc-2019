from day_03 import *


def test_shortest_distance_to_intersection_from_origin():
    assert (shortest_distance_to_intersection_from_origin("R8,U5,L5,D3".split(','), "U7,R6,D4,L4".split(',')) == 6)
    assert (shortest_distance_to_intersection_from_origin(
        "R75,D30,R83,U83,L12,D49,R71,U7,L72".split(','),
        "U62,R66,U55,R34,D71,R55,D58,R83".split(',')) == 159)
    assert (shortest_distance_to_intersection_from_origin(
        "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51".split(','),
        "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7".split(',')) == 135)


def test_shortest_steps_to_intersection_on_paths():
    assert (shortest_steps_to_intersection_on_paths("R8,U5,L5,D3".split(','), "U7,R6,D4,L4".split(',')) == 30)
    assert (shortest_steps_to_intersection_on_paths(
        "R75,D30,R83,U83,L12,D49,R71,U7,L72".split(','),
        "U62,R66,U55,R34,D71,R55,D58,R83".split(',')) == 610)
    assert (shortest_steps_to_intersection_on_paths(
        "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51".split(','),
        "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7".split(',')) == 410)
