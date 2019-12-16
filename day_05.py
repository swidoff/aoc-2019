import fileinput
from dataclasses import dataclass
from enum import Enum
from typing import List


class Opcode(Enum):
    ADD = 1
    MUTLIPLY = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    HALT = 99


class ParameterMode(Enum):
    POSITION = 0
    IMMEDIATE = 1


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


def run_program(program: List[int], input: List[int]) -> List[int]:
    program_counter = 0
    input_counter = 0
    output = []

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
            program[program[program_counter + 1]] = input[input_counter]
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
                write(3, 1)
            else:
                write(3, 0)
            program_counter += 4
        elif instruction.opcode == Opcode.OUTPUT:
            output.append(param_at(instruction.mode_at(0), 1))
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
    program = list(program_in_file("day_05_input.txt"))
    input = [1]
    output = run_program(program, input)
    return output


def problem2():
    program = list(program_in_file("day_05_input.txt"))
    input = [5]
    output = run_program(program, input)
    return output


if __name__ == '__main__':
    print(problem1())
    print(problem2())
