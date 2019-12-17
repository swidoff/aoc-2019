from functools import partial
from itertools import repeat
from typing import List

from segment_tree import SegmentTree
from toolz import pipe

phase = 1


def fft_phase(input_signal: List[int], offset: int = 0) -> List[int]:
    global phase
    print('phase ' + str(phase))
    phase += 1
    pattern = (0, 1, 0, -1)
    n = len(input_signal)

    res = []
    if offset > 0:
        res.extend([0] * offset)

    tree = SegmentTree(input_signal[offset:])
    for i in range(offset, n):
        sum_prod = 0
        d, p, pat_repeat = 0, 0, i
        while d < n:
            pat_digit = pattern[p % 4]
            if pat_digit != 0:
                mult = 1 if pat_digit > 0 else -1
                digit_sum = tree.query(d - offset, min(d + pat_repeat, n) - offset - 1, "sum")
                # digit_sum = sum(input_signal[d - offset: min(d + pat_repeat, n) - offset])
                sum_prod += digit_sum * mult
            d += pat_repeat
            p += 1
            pat_repeat = i + 1

        digit = abs(sum_prod) % 10
        res.append(digit)

    return res


def fft(input_signal: str, phases: int = 100) -> str:
    res = pipe([int(c) for c in input_signal], *repeat(fft_phase, phases))
    return ''.join(str(d) for d in res)


def problem1():
    with open('day_16_input.txt') as f:
        input_signal = f.readline().strip()
        return fft(input_signal, 100)[:8]


def fft2(input_signal: str) -> str:
    offset = int(input_signal[:7])
    input_signal = [int(c) for c in input_signal] * 10000
    res = pipe(input_signal, *repeat(partial(fft_phase, offset=offset), 100))
    return ''.join(str(d) for d in res[offset:offset + 8])


def problem2():
    with open('day_16_input.txt') as f:
        input_signal = f.readline().strip()
        return fft2(input_signal)


if __name__ == '__main__':
    # print(problem1())
    print(problem2())
    # print(fft2('03036732577212944063491565474664'))
    # print(fft2('02935109699940807407585447034323'))
    # print(fft2('03081770884921959731165446850517'))
