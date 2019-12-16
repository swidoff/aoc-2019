import fileinput


def fuel(mass: int) -> int:
    return mass // 3 - 2


def total_fuel(mass: int) -> int:
    mass_fuel = fuel(mass)
    if mass_fuel <= 0:
        return 0
    else:
        return mass_fuel + total_fuel(mass_fuel)


def lines(file: str):
    with fileinput.input(files=(file,)) as f:
        for line in f:
            yield line.strip()


def problem_1():
    return sum(fuel(int(l)) for l in lines('day_01_input.txt'))


def problem_2():
    return sum(total_fuel(int(l)) for l in lines('day_01_input.txt'))


if __name__ == '__main__':
    print(problem_1())
    print(problem_2())
