from functools import partial
from typing import List, Tuple, Callable
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

    # print(cards[2019])
    for line in program.split('\n'):
        for exp, func in table.items():
            match = re.match(exp, line)
            if match:
                groups = match.groups()
                cards = func(cards, *map(int, groups))
                # print(cards[2019])

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
    #
    return new_pos
    # return (pos + n + num_cards) % num_cards


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
    # return modinv(inc, num_cards) * pos % num_cards  # modinv is modular inverse


def run_program_reverse(program: str, num_cards: int, pos: int) -> int:
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


# The following ideas were lifted from here:
# https://www.reddit.com/r/adventofcode/comments/ee0rqi/2019_day_22_solutions/fbnifwk/


# From https://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


def to_linear_function(f: Callable[[int], int], x: int, d: int) -> Tuple[int, int]:
    """
    Defines the linear function f(i) as f(i) = A(i) + B

     A*X+B = Y
     A*Y+B = Z
     A*(X-Y) = Y-Z
     A = (Y-Z)/(X-Y)
     B = Y-A*X
    """
    y = f(x)
    z = f(y)
    a = (y - z) * modinv(x - y + d, d) % d
    b = (y - a * x) % d
    return a, b


def repeat_linear_function(a: int, b: int, d: int, n: int, x: int) -> int:
    return (pow(a, n, d) * x + (pow(a, n, d) - 1) * modinv(a - 1, d) * b) % d


def problem2():
    with open('day_22_input.txt') as f:
        program = f.read()

    num_cards = 119315717514047
    repeats = 101741582076661
    pos = 2020

    # num_cards = 10007
    # repeats = 2
    # pos = 6638

    f = partial(run_program_reverse, program, num_cards)
    a, b = to_linear_function(f, pos, num_cards)
    res = repeat_linear_function(a, b, num_cards, repeats, pos)

    # print(run_program(program + "\n" + program)[6638])
    # print(run_program(program)[6638])

    return res


if __name__ == '__main__':
    # print(problem1())
    print(problem2())  # NOT: 38776749976433
