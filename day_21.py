from typing import Union, List

from day_11 import run_program_coroutine, program_in_file


def run_springcode(intcode: List[int], springcode: str) -> Union[int, str]:
    output = []

    def record_output():
        while True:
            o = (yield)
            output.append(o)

    recorder = record_output()
    next(recorder)

    runner = run_program_coroutine(list(intcode), recorder)
    next(runner)

    try:
        for c in springcode:
            runner.send(ord(c))
    except StopIteration:
        pass

    return ''.join(chr(c) for c in output) if 0 <= output[-1] < 255 else output[-1]


def problem1():
    """
    There is a hole in any of A B or C and there is a safe place to land on D
    (NOT A) OR (NOT B) OR (NOT C) AND D
    """
    spring_code = """
NOT A J
NOT B T
OR T J
NOT C T
OR T J
AND D J
WALK
"""
    program = list(program_in_file('day_21_input.txt'))
    print(run_springcode(program, spring_code[1:]))


def problem2():
    """
    THe same as above, but also we are not "stuck" where the next space E is a hole and so we are forced to jump, but
    the landing spot H is a hole.
    (NOT A) OR (NOT B) OR (NOT C) AND D AND (E or H)

    E is land or H is land
    """
    spring_code = """
NOT A J
NOT B T
OR T J
NOT C T
OR T J
AND D J
AND E T
OR H T
AND T J
RUN
"""
    program = list(program_in_file('day_21_input.txt'))
    print(run_springcode(program, spring_code[1:]))


if __name__ == '__main__':
    # problem1()  # 19350258
    problem2() # 1142627861
