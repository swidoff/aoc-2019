import fileinput
from collections import Counter
from dataclasses import dataclass
from typing import List, Iterator

from more_itertools import take, first


@dataclass
class Image(object):
    rows: int
    columns: int
    layers: List[List[int]]


def read_image(digits: Iterator[int], rows: int, columns: int):
    layers = []
    while True:
        layer = list(take(rows * columns, digits))
        if len(layer) == 0:
            break
        elif len(layer) < rows * columns:
            raise ValueError(f"Layer has fewer than {rows * columns} digits: {len(layer)}")
        else:
            layers.append(layer)

    return Image(rows, columns, layers)


def digits_in_file(file: str):
    with fileinput.input(files=(file,)) as f:
        for line in f:
            for c in line.strip():
                yield int(c)


def problem1():
    image = read_image(digits_in_file('day_08_input.txt'), 6, 25)
    counters = [Counter(layer) for layer in image.layers]
    min_zeroes = min(c[0] for c in counters)
    min_zeroes_index = min(i for i, c in enumerate(counters) if c[0] == min_zeroes)
    min_zeroes_counter = counters[min_zeroes_index]
    return min_zeroes_counter[1] * min_zeroes_counter[2]


def decode(image: Image) -> str:
    message = (
        first(p for p in pixels if p != 2)
        for pixels in zip(*image.layers)
    )

    return "\n".join(
        str.join('', (' ' if d == 0 else '*' for d in take(image.columns, message)))
        for _ in range(0, image.rows)
    )


def problem2() -> str:
    image = read_image(digits_in_file('day_08_input.txt'), 6, 25)
    return decode(image)


if __name__ == '__main__':
    print(problem1())
    print(problem2())
