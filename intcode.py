import fileinput
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from typing import List


def read(file: str):
    with fileinput.input(files=(file,)) as f:
        for line in f:
            for c in line.split(','):
                yield int(c)


class Opcode(Enum):
    ADD = 1
    MUL = 2
    IN = 3
    OUT = 4
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

    def __call__(self, *args, **kwargs):
        index = args[0]
        return self.modes[index] if index < len(self.modes) else ParameterMode.POSITION


def parse_instruction(opcode: int) -> Instruction:
    opstr = str(opcode)
    instruction = Opcode(int(opstr[-2:]))
    modes = [ParameterMode(int(m)) for m in reversed(opstr[:-2])]
    return Instruction(instruction, modes)


def run(program_in: List[int]):
    program = defaultdict(lambda: 0, dict(enumerate(program_in)))
    program_counter = 0
    relative_base = 0
    output = []

    def get(i: Instruction, offset: int) -> int:
        value = program[program_counter + offset]
        mode = i(offset - 1)
        if mode == ParameterMode.POSITION:
            res = program[value]
        elif mode == ParameterMode.IMMEDIATE:
            res = value
        else:  # if mode == ParameterMode.RELATIVE:
            res = program[value + relative_base]
        return res

    def set(i: Instruction, offset: int, val: int):
        param = program[program_counter + offset]
        pos = relative_base + param if i(offset - 1) == ParameterMode.RELATIVE else param
        program[pos] = val

    while True:
        if program_counter >= len(program):
            raise ValueError("counter has moved passed the end of the list")

        i = parse_instruction(program[program_counter])

        if i.opcode == Opcode.ADD:
            set(i, 3, get(i, 1) + get(i, 2))
            program_counter += 4
        elif i.opcode == Opcode.MUL:
            set(i, 3, get(i, 1) * get(i, 2))
            program_counter += 4
        elif i.opcode == Opcode.IN:
            value = yield
            set(i, 1, value)
            program_counter += 2
        elif i.opcode == Opcode.OUT:
            yield get(i, 1)
            program_counter += 2
        elif i.opcode == Opcode.JUMP_IF_TRUE or i.opcode == Opcode.JUMP_IF_FALSE:
            param = get(i, 1)
            if (param != 0 and i.opcode == Opcode.JUMP_IF_TRUE) or \
                    (param == 0 and i.opcode == Opcode.JUMP_IF_FALSE):
                program_counter = get(i, 2)
            else:
                program_counter += 3
        elif i.opcode == Opcode.LESS_THAN or i.opcode == Opcode.EQUALS:
            param1 = get(i, 1)
            param2 = get(i, 2)
            if (i.opcode == Opcode.LESS_THAN and param1 < param2) or \
                    (i.opcode == Opcode.EQUALS and param1 == param2):
                set(i, 3, 1)
            else:
                set(i, 3, 0)
            program_counter += 4
        elif i.opcode == Opcode.RELATIVE_BASE_OFFSET:
            relative_base += get(i, 1)
            program_counter += 2
        elif i.opcode == Opcode.HALT:
            break
        else:
            raise ValueError("Unknown op_code: " + str(i))

    return output
