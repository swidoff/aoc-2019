from collections import defaultdict
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Tuple

from day_09 import ParameterMode, parse_instruction, Opcode, program_in_file


def run_program_coroutine(program_in: List[int], output_coroutine):
    program = defaultdict(lambda: 0, dict(enumerate(program_in)))
    program_counter = 0
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
            value = (yield)
            write(instruction.mode_at(0), 1, value)
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
                write(instruction.mode_at(2), 3, 1)
            else:
                write(instruction.mode_at(2), 3, 0)
            program_counter += 4
        elif instruction.opcode == Opcode.RELATIVE_BASE_OFFSET:
            relative_base += param_at(instruction.mode_at(0), 1)
            program_counter += 2
        elif instruction.opcode == Opcode.HALT:
            break
        else:
            raise ValueError("Unknown op_code: " + str(instruction))

    return output


class Direction(Enum):
    UP = 0
    LEFT = 1
    DOWN = 2
    RIGHT = 3

    def turn(self, turn_value):
        if turn_value == 0:
            return Direction((self.value + 1) % 4)
        elif turn_value == 1:
            new_value = self.value - 1
            return Direction(new_value if new_value >= 0 else 3)

    def move(self, point: Tuple[int, int]) -> Tuple[int, int]:
        if self == Direction.UP:
            return point[0], point[1] - 1
        elif self == Direction.LEFT:
            return point[0] - 1, point[1]
        elif self == Direction.DOWN:
            return point[0], point[1] + 1
        else:
            return point[0] + 1, point[1]


@dataclass
class Robot:
    position: Tuple[int, int] = (0, 0)
    direction: Direction = Direction.UP
    painted: Dict[Tuple[int, int], int] = field(default_factory=dict)


def paint(program: List[int], robot=Robot()) -> Robot:
    def move_robot():
        while True:
            color_value = (yield)
            turn_value = (yield)
            robot.painted[robot.position] = color_value
            robot.direction = robot.direction.turn(turn_value)
            robot.position = robot.direction.move(robot.position)

    robot_coroutine = move_robot()
    next(robot_coroutine)

    computer = run_program_coroutine(program, robot_coroutine)
    next(computer)

    while True:
        try:
            color_value = robot.painted.get(robot.position, 0)
            computer.send(color_value)
        except StopIteration:
            break

    return robot


def problem1():
    program = program_in_file('day_11_input.txt')
    robot = paint(program)
    return len(robot.painted)


def render(painted: Dict[Tuple[int, int], int]) -> str:
    max_x = max(p[0] for p in painted) + 1
    max_y = max(p[1] for p in painted) + 1
    m = []
    for _ in range(0, max_y):
        m.append([' ' for _ in range(0, max_x)])

    for (x, y), c in painted.items():
        s = '*' if c else ' '
        m[y][x] = s

    res = '\n'.join(''.join(r) for r in m)
    return res


def problem2():
    program = program_in_file('day_11_input.txt')
    robot = paint(program, Robot(painted={(0, 0): 1}))
    return render(robot.painted)


if __name__ == '__main__':
    # print(problem1())
    print(problem2())
