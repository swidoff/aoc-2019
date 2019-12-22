from day_22 import run_program, run_program_reverse


def test_run_program():
    program = """
deal with increment 7
deal into new stack
deal into new stack
"""
    assert run_program(program[1:], tuple(range(0, 10))) == (0, 3, 6, 9, 2, 5, 8, 1, 4, 7)

    program = """
cut 6
deal with increment 7
deal into new stack
"""
    assert run_program(program[1:], tuple(range(0, 10))) == (3, 0, 7, 4, 1, 8, 5, 2, 9, 6)

    program = """
deal with increment 7
deal with increment 9
cut -2
"""
    assert run_program(program[1:], tuple(range(0, 10))) == (6, 3, 0, 7, 4, 1, 8, 5, 2, 9)

    program = """
deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1
"""
    assert run_program(program[1:], tuple(range(0, 10))) == (9, 2, 5, 8, 1, 4, 7, 0, 3, 6)


def test_run_program_reverse():
    program = """
deal with increment 7
deal into new stack
deal into new stack
"""
    for pos, val in enumerate((0, 3, 6, 9, 2, 5, 8, 1, 4, 7)):
        assert run_program_reverse(program[1:], 10, pos) == val

    program = """
cut 6
deal with increment 7
deal into new stack
"""
    for pos, val in enumerate((3, 0, 7, 4, 1, 8, 5, 2, 9, 6)):
        assert run_program_reverse(program[1:], 10, pos) == val

    program = """
deal with increment 7
deal with increment 9
cut -2
"""

    for pos, val in enumerate((6, 3, 0, 7, 4, 1, 8, 5, 2, 9)):
        assert run_program_reverse(program[1:], 10, pos) == val

    program = """
deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1
"""

    for pos, val in enumerate((9, 2, 5, 8, 1, 4, 7, 0, 3, 6)):
        assert run_program_reverse(program[1:], 10, pos) == val
