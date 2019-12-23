from collections import deque
from typing import List

from day_11 import run_program_coroutine, program_in_file


def simulate_network(program: List[int]):
    n = 50
    queues = [deque() for _ in range(n)]
    res = []

    def router():
        while True:
            dest = (yield)
            x = (yield)
            y = (yield)
            if dest == 255:
                res.append((x, y))
                break
            else:
                queues[dest].append((x, y))

    computers = []
    for i in range(50):
        r = router()
        next(r)

        computer = run_program_coroutine(list(program), r)
        next(computer)
        computer.send(i)
        computers.append(computer)

    try:
        while not res:
            for i, comp in enumerate(computers):
                q = queues[i]
                if q:
                    while q:
                        x, y, = q.popleft()
                        comp.send(x)
                        comp.send(y)
                else:
                    comp.send(-1)
    except StopIteration:
        pass

    return res[0]


def problem1():
    program = list(program_in_file('day_23_input.txt'))
    return simulate_network(program)


def simulate_network_with_nat(program: List[int]):
    n = 50
    queues = [deque() for _ in range(n)]
    nat = [(-1, -1)]
    last_nat = []
    res = None

    def router():
        while True:
            dest = (yield)
            x = (yield)
            y = (yield)
            if dest == 255:
                nat[0] = (x, y)
            else:
                queues[dest].append((x, y))

    def new_computer(i):
        r = router()
        next(r)
        computer = run_program_coroutine(list(program), r)
        next(computer)
        computer.send(i)
        return computer

    computers = [new_computer(i) for i in range(50)]

    try:
        while not res:
            for i, comp in enumerate(computers):
                q = queues[i]
                if q:
                    while q:
                        x, y = q.popleft()
                        comp.send(x)
                        comp.send(y)
                else:
                    comp.send(-1)

            if not any(queues):
                x, y = nat[0]
                if last_nat and last_nat[1] == y:
                    res = nat
                else:
                    last_nat = (x, y)
                    computers[0].send(x)
                    computers[0].send(y)
    except StopIteration:
        pass

    return res


def problem2():
    program = list(program_in_file('day_23_input.txt'))
    return simulate_network_with_nat(program)


if __name__ == '__main__':
    # print(problem1())
    print(problem2())
