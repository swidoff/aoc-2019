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


if __name__ == '__main__':
    problem1()  # 19350258
