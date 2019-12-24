from day_24 import BugGrid, initial_grid, recursive_steps, recursive_count_bugs, grid_to_str


def test_first_repeated_bits():
    start = """
....#
#..#.
#..##
..#..
#....
"""
    expected = """
.....
.....
.....
#....
.#...
"""
    grid = BugGrid(n=5)
    start_bits = grid.str_to_bits(start[1:-1])
    actual_bits = grid.first_repeated_bits(start_bits, verbose=False)
    actual = grid.bits_to_str(actual_bits)
    assert expected[1:-1] == actual


def test_recursive_bug_count():
    start = """
....#
#..#.
#..##
..#..
#....
"""
    grid = initial_grid(start[1:-1])
    final = recursive_steps(grid, 10)
    for i, grid in enumerate(final):
        print(f"Depth {i - 5}")
        print(grid_to_str(grid))
        print()

    assert recursive_count_bugs(final) == 99
