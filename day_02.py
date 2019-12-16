import fileinput
from itertools import product
from typing import List


def run_program(ls: List[int]) -> List[int]:
    counter = 0
    while True:
        if counter >= len(ls):
            raise ValueError("counter has moved passed the end of the list")

        op_code = ls[counter]
        if op_code == 1:
            res = ls[ls[counter + 1]] + ls[ls[counter + 2]]
            ls[ls[counter + 3]] = res
        elif op_code == 2:
            res = ls[ls[counter + 1]] * ls[ls[counter + 2]]
            ls[ls[counter + 3]] = res
        elif op_code == 99:
            break
        else:
            raise ValueError("Unknown op_code: " + str(op_code))

        counter += 4

    return ls


def ints_in_file(file: str):
    with fileinput.input(files=(file,)) as f:
        for line in f:
            for c in line.split(','):
                yield int(c)


def run_program_with_parameters(in_ls: List[int], noun: int, verb: int) -> int:
    ls = list(in_ls)
    ls[1] = noun
    ls[2] = verb
    res = run_program(ls)
    return res[0]


def problem_1():
    ls = list(ints_in_file('day_02_input.txt'))
    return run_program_with_parameters(ls, 12, 2)


def problem_2():
    ls = list(ints_in_file('day_02_input.txt'))
    params = product(list(range(0, 100)), list(range(0, 100)))
    for noun, verb in params:
        if run_program_with_parameters(ls, noun, verb) == 19690720:
            return 100 * noun + verb
    return None


if __name__ == '__main__':
    print(problem_1())
    print(problem_2())
