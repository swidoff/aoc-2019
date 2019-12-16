import operator
from typing import List
from itertools import cycle, repeat
from more_itertools import flatten
from toolz import drop, pipe


def fft_phase(input_signal: List[int], base_pattern=None) -> List[int]:
    if base_pattern is None:
        base_pattern = [0, 1, 0, -1]

    res = []
    repeating_pattern = list(base_pattern)
    for i in range(len(input_signal)):
        sum_prod = sum(map(lambda p: operator.mul(*p), zip(input_signal, drop(1, cycle(repeating_pattern)))))
        digit = abs(sum_prod) % 10
        res.append(digit)
        repeating_pattern = list(flatten([[d] * (i + 2) for d in base_pattern]))

    return res


def fft(input_signal: str, phases: int = 100) -> str:
    res = pipe([int(c) for c in input_signal], *repeat(fft_phase, phases))
    return ''.join(str(d) for d in res)


def problem1():
    with open('day_16_input.txt') as f:
        input_signal = f.readline().strip()
        return fft(input_signal, 100)[:8]


if __name__ == '__main__':
    print(problem1())
