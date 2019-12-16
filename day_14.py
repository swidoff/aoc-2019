from collections import defaultdict
from dataclasses import dataclass
from io import StringIO
from typing import Tuple, List, Dict


@dataclass(frozen=True)
class Quantity(object):
    chemical: str
    amount: int


@dataclass(frozen=True)
class Equation(object):
    output: Quantity
    inputs: Tuple[Quantity, ...]


def parse_quantity(q) -> Quantity:
    amount, chemical = q.split(' ')
    return Quantity(chemical, int(amount))


def read_equations(file) -> List[Equation]:
    res = []

    f = open(file) if not isinstance(file, StringIO) else file

    line = f.readline()
    while line:
        if len(line.strip()) > 0:
            lhs, rhs = line.strip().split(' => ')
            eq = Equation(parse_quantity(rhs), tuple(parse_quantity(q) for q in lhs.split(', ')))
            res.append(eq)

        line = f.readline()

    f.close()
    return res


def ore_for_fuel(equations: List[Equation], fuel: int = 1) -> (int, Dict[str, int]):
    eq_table = {
        eq.output.chemical: eq
        for eq in equations
    }
    store = defaultdict(lambda: 0)
    ore = 0

    queue = [Quantity('FUEL', fuel)]
    while queue:
        q = queue.pop()
        eq = eq_table[q.chemical]
        needed = q.amount
        remainder = needed - store.get(q.chemical, 0)
        if remainder > 0:
            output = eq.output.amount
            iterations = remainder // output if remainder % output == 0 else (remainder // output) + 1
            store[q.chemical] += output * iterations
            for i in eq.inputs:
                if i.chemical == 'ORE':
                    ore += i.amount * iterations
                else:
                    queue.append(Quantity(i.chemical, i.amount * iterations))

        store[q.chemical] -= needed

    return ore


def problem1():
    equations = read_equations('day_14_input.txt')
    ore = ore_for_fuel(equations)
    return ore


def fuel_for_ore(equations: List[Equation], ore: int) -> int:
    min_fuel = 0
    max_fuel = ore
    best = 0

    while min_fuel <= max_fuel:
        midpoint = (max_fuel + min_fuel) // 2
        cost = ore_for_fuel(equations, fuel=midpoint)
        if cost > ore:
            max_fuel = midpoint - 1
        else:
            best = midpoint
            min_fuel = midpoint + 1

    return best


def problem2():
    equations = read_equations('day_14_input.txt')
    fuel = fuel_for_ore(equations, 1000000000000)
    return fuel


if __name__ == '__main__':
    print(problem1())
    print(problem2())
