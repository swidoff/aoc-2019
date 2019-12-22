from functools import partial
from typing import List, Tuple
import re


def cut(cards: Tuple[int, ...], n: int) -> Tuple[int, ...]:
    return cards[n:] + cards[:n]


def deal_into_new_stack(cards: Tuple[int, ...]) -> Tuple[int, ...]:
    return tuple(reversed(cards))


def deal_with_increment(cards: Tuple[int, ...], inc: int) -> Tuple[int, ...]:
    res = list(cards)
    pos = 0
    for c in cards:
        res[pos % len(cards)] = c
        pos += inc
    return tuple(res)


def run_program(program: str, cards: Tuple[int, ...] = tuple(range(0, 10007))) -> Tuple[int, ...]:
    table = {
        r'cut (-?\d+)': cut,
        r'deal into new stack': deal_into_new_stack,
        r'deal with increment (\d+)': deal_with_increment
    }

    print(cards[2019])
    for line in program.split('\n'):
        for exp, func in table.items():
            match = re.match(exp, line)
            if match:
                groups = match.groups()
                cards = func(cards, *map(int, groups))
                print(cards[2019])

    return cards


def problem1():
    with open('day_22_input.txt') as f:
        program = f.read()

    cards = run_program(program)
    orig = run_program_reverse(program, num_cards=10007, pos=6638)
    return cards.index(2019), orig


def reverse_cut(num_cards: int, pos: int, n: int) -> int:
    """Returns where the card at pos will be when the cut is reversed."""
    if n > 0:
        if pos < num_cards - n:
            new_pos = n + pos
        else:
            new_pos = pos - (num_cards - n)
    else:
        if pos < abs(n):
            # Came from the back of the deck.
            new_pos = pos + (num_cards - abs(n))
        else:
            # Came from the front of the deck.
            new_pos = pos - abs(n)

    return new_pos


def reverse_deal_into_new_stack(num_cards: int, pos: int) -> int:
    return num_cards - pos - 1


def reverse_deal_with_increment(num_cards: int, pos: int, inc: int) -> int:
    i = 0
    guess = (i * num_cards + pos) / inc
    while guess < num_cards:
        if guess == int(guess):
            return int(guess)
        i += 1
        guess = (i * num_cards + pos) / inc
    raise ValueError("Failed to reverse deal with increment")


def run_program_reverse(program: str, num_cards: int = 119315717514047, pos: int = 2020) -> int:
    table = {
        r'cut (-?\d+)': partial(reverse_cut, num_cards),
        r'deal into new stack': partial(reverse_deal_into_new_stack, num_cards),
        r'deal with increment (\d+)': partial(reverse_deal_with_increment, num_cards)
    }

    res = pos
    for line in reversed(program.split('\n')):
        for exp, func in table.items():
            match = re.match(exp, line)
            if match:
                groups = match.groups()
                res = func(res, *map(int, groups))

    return res


def problem2():
    with open('day_22_input.txt') as f:
        program = f.read()

    seen = set()
    pos = 2020
    # for i in range(101741582076661):
    for i in range(100000000):
        if (i % 1000000) == 0:
            print(i)

        pos = run_program_reverse(program, pos=pos)
        if pos in seen:
            print('seen it! ' + str(pos))
        elif pos == 2020:
            print('Perfect shuffle atfer ' + str(i) + " iterations ")
        else:
            seen.add(pos)
    return pos


if __name__ == '__main__':
    print(problem1())
    # print(problem2())
