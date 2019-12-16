from functools import partial, reduce
from inspect import getgeneratorstate
from itertools import permutations
from typing import List
from day_05 import program_in_file, run_program, ParameterMode, parse_instruction, Opcode


def amplify(program: List[int], phases: List[int]) -> int:
    run = partial(run_program, program)
    return reduce(lambda output, phase: run([phase, output])[-1], phases, 0)


def max_amplify(program: List[int], amplifiers: int = 5) -> int:
    return max(
        amplify(program, phases)
        for phases in permutations(list(range(0, amplifiers)))
    )


def problem1():
    return max_amplify(list(program_in_file('day_07_input.txt')))


def run_program_coroutine(program: List[int], output_coroutine):
    program_counter = 0

    def param_at(mode: ParameterMode, offset: int) -> int:
        value = program[program_counter + offset]
        return program[value] if mode == ParameterMode.POSITION else value

    def write(offset: int, value: int):
        program[program[program_counter + offset]] = value

    while True:
        if program_counter >= len(program):
            raise ValueError("counter has moved passed the end of the list")

        instruction = parse_instruction(program[program_counter])

        if instruction.opcode == Opcode.ADD:
            write(3, param_at(instruction.mode_at(0), 1) + param_at(instruction.mode_at(1), 2))
            program_counter += 4
        elif instruction.opcode == Opcode.MUTLIPLY:
            write(3, param_at(instruction.mode_at(0), 1) * param_at(instruction.mode_at(1), 2))
            program_counter += 4
        elif instruction.opcode == Opcode.INPUT:
            input_value = (yield)
            write(1, input_value)
            program_counter += 2
        elif instruction.opcode == Opcode.OUTPUT:
            try:
                output_coroutine.send(param_at(instruction.mode_at(0), 1))
            except StopIteration:
                pass
            program_counter += 2
        elif instruction.opcode == Opcode.JUMP_IF_TRUE or instruction.opcode == Opcode.JUMP_IF_FALSE:
            param = param_at(instruction.mode_at(0), 1)
            if (param != 0 and instruction.opcode == Opcode.JUMP_IF_TRUE) or \
                    (param == 0 and instruction.opcode == Opcode.JUMP_IF_FALSE):
                program_counter = param_at(instruction.mode_at(1), 2)
            else:
                program_counter += 3
        elif instruction.opcode == Opcode.LESS_THAN or instruction.opcode == Opcode.EQUALS:
            param1 = param_at(instruction.mode_at(0), 1)
            param2 = param_at(instruction.mode_at(1), 2)
            if (instruction.opcode == Opcode.LESS_THAN and param1 < param2) or \
                    (instruction.opcode == Opcode.EQUALS and param1 == param2):
                write(3, 1)
            else:
                write(3, 0)
            program_counter += 4
        elif instruction.opcode == Opcode.HALT:
            break
        else:
            raise ValueError("Unknown op_code: " + str(instruction))


def amplify_wth_feedback(program: List[int], phases: List[int]) -> int:
    signal = [0]

    def output_coroutine():
        while True:
            value = (yield)
            signal.append(value)

    chain = output_coroutine()
    next(chain)
    for p in reversed(phases):
        a = run_program_coroutine(list(program), chain)
        next(a)
        a.send(p)
        chain = a

    try:
        while True:
            chain.send(signal[-1])
    except StopIteration:
        pass

    return signal[-1]


def max_amplify_with_feedback(program: List[int], amplifiers: int = 5) -> int:
    return max(
        amplify_wth_feedback(program, phases)
        for phases in permutations(list(range(5, 5 + amplifiers)))
    )


def problem2():
    return max_amplify_with_feedback(list(program_in_file('day_07_input.txt')))


if __name__ == '__main__':
    print(problem1())
    print(problem2())
