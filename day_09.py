import fileinput
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict


class Opcode(Enum):
    ADD = 1
    MUTLIPLY = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    RELATIVE_BASE_OFFSET = 9
    HALT = 99


class ParameterMode(Enum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2


@dataclass
class Instruction(object):
    opcode: Opcode
    modes: List[ParameterMode]

    def mode_at(self, index: int):
        return self.modes[index] if index < len(self.modes) else ParameterMode.POSITION


def parse_instruction(opcode: int) -> Instruction:
    opstr = str(opcode)
    instruction = Opcode(int(opstr[-2:]))
    modes = [ParameterMode(int(m)) for m in reversed(opstr[:-2])]
    return Instruction(instruction, modes)


def run_program(program_in: List[int], input: List[int]) -> List[int]:
    program = defaultdict(lambda: 0, dict(enumerate(program_in)))
    program_counter = 0
    input_counter = 0
    relative_base = 0
    output = []

    def param_at(mode: ParameterMode, offset: int) -> int:
        value = program[program_counter + offset]
        if mode == ParameterMode.POSITION:
            res = program[value]
        elif mode == ParameterMode.IMMEDIATE:
            res = value
        else:  # if mode == ParameterMode.RELATIVE:
            res = program[value + relative_base]
        return res

    def write(mode: ParameterMode, offset: int, value: int):
        param = program[program_counter + offset]
        pos = relative_base + param if mode == ParameterMode.RELATIVE else param
        program[pos] = value

    while True:
        if program_counter >= len(program):
            raise ValueError("counter has moved passed the end of the list")

        instruction = parse_instruction(program[program_counter])

        if instruction.opcode == Opcode.ADD:
            write(instruction.mode_at(2), 3, param_at(instruction.mode_at(0), 1) + param_at(instruction.mode_at(1), 2))
            program_counter += 4
        elif instruction.opcode == Opcode.MUTLIPLY:
            write(instruction.mode_at(2), 3, param_at(instruction.mode_at(0), 1) * param_at(instruction.mode_at(1), 2))
            program_counter += 4
        elif instruction.opcode == Opcode.INPUT:
            write(instruction.mode_at(0), 1, input[input_counter])
            program_counter += 2
            input_counter += 1
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
                write(instruction.mode_at(2), 3, 1)
            else:
                write(instruction.mode_at(2), 3, 0)
            program_counter += 4
        elif instruction.opcode == Opcode.OUTPUT:
            output.append(param_at(instruction.mode_at(0), 1))
            program_counter += 2
        elif instruction.opcode == Opcode.RELATIVE_BASE_OFFSET:
            relative_base += param_at(instruction.mode_at(0), 1)
            program_counter += 2
        elif instruction.opcode == Opcode.HALT:
            break
        else:
            raise ValueError("Unknown op_code: " + str(instruction))

    return output


def program_in_file(file: str):
    with fileinput.input(files=(file,)) as f:
        for line in f:
            for c in line.split(','):
                yield int(c)


def problem1():
    return run_program(list(program_in_file('day_09_input.txt')), [1])


def problem2():
    return run_program(list(program_in_file('day_09_input.txt')), [2])


if __name__ == '__main__':
    print(problem1())
    print(problem2())
