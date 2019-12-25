from itertools import combinations
from typing import List

from more_itertools import flatten

from day_11 import run_program_coroutine, program_in_file


def play_zork(program: List[int], script: List[str] = None):
    buf = []

    def screen():
        while True:
            i = yield
            c = chr(i)
            if c == '\n':
                print(''.join(buf))
                buf.clear()
            else:
                buf.append(c)

    scr = screen()
    next(scr)

    computer = run_program_coroutine(program, scr)
    next(computer)

    def send_command(cmd: str):
        for c in cmd:
            computer.send(ord(c))
        computer.send(ord('\n'))

    try:
        if script:
            for command in script:
                send_command(command)

        while True:
            command = input()
            send_command(command)
    except StopIteration:
        pass


collect_items = [
    "west",
    "take hologram",
    "north",
    "take space heater",
    "east",
    "take space law space brochure",
    "east",
    "take tambourine",
    "west",
    "west",
    "south",
    "east",
    "east",
    "take festive hat",
    "east",
    "take food ration",
    "east",
    "take spool of cat6",
    "west",
    "west",
    "south",
    "east",
    "east",
    # "take fuel cell",
    "east"
]

inventory = [
    # "fuel cell",
    "space heater",
    "hologram",
    "space law space brochure",
    "food ration",
    "tambourine",
    "spool of cat6",
    "festive hat"
]


def try_combinations(n: int) -> List[str]:
    res = [f"drop {item}" for item in inventory]
    for comb in combinations(inventory, n):
        for item in comb:
            res.append(f"take {item}")
        res.append("south")
        for item in comb:
            res.append(f"drop {item}")
    return res


def problem1():
    program = list(program_in_file('day_25_input.txt'))
    play_zork(program, script=collect_items + try_combinations(4))


if __name__ == '__main__':
    problem1()
