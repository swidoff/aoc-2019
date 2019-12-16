import operator
from functools import partial
from typing import List
from itertools import cycle, repeat
from more_itertools import flatten
from toolz import drop, pipe, take
import numpy as np

from day_12 import lcm


def fft_phase(input_signal: List[int], repetitions: int = 1, base_pattern=None) -> List[int]:
    if base_pattern is None:
        base_pattern = [0, 1, 0, -1]

    print('phase')
    res = []
    n = len(input_signal)
    total_n = n * repetitions
    repeating_pattern = list(base_pattern)
    for i in range(total_n):
        pat_len = len(repeating_pattern)
        cycle_len = min(total_n, lcm(n, pat_len))
        multiples = total_n // cycle_len

        sum_prod = 0
        d = i
        p = 1 + i
        while d < cycle_len:
            sum_prod += input_signal[d % n] * repeating_pattern[p % pat_len]
            d += 1
            p += 1

        sum_prod *= multiples

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


def fft2(input_signal: str, phases: int = 100) -> str:
    offset = int(input_signal[:7])
    input_signal = [int(c) for c in input_signal]
    res = pipe(input_signal, *repeat(partial(fft_phase, repetitions=10000), phases))
    return ''.join(str(d) for d in res[offset:offset + 8])


def problem2():
    with open('day_16_input.txt') as f:
        input_signal = f.readline().strip()
        return fft2(input_signal)


if __name__ == '__main__':
    # print(problem1())
    # print(problem2())
    print(fft2('03036732577212944063491565474664'))
