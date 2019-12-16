from typing import Iterator


def contains_repeated_digits(password_str: str):
    return any(map(lambda t: t[0] == t[1], zip(password_str, password_str[1:])))


def no_decrease(password_str):
    return all(map(lambda t: t[0] <= t[1], zip(password_str, password_str[1:])))


def valid_password1(password: int) -> bool:
    password_str = str(password)
    return len(password_str) == 6 and contains_repeated_digits(password_str) and no_decrease(password_str)


def matching_digit_group_lens(password_str: str) -> Iterator[int]:
    prev = password_str[0]
    count = 1
    for c in password_str[1:]:
        if c == prev:
            count += 1
        else:
            yield count
            count = 1
            prev = c

    if count > 1:
        yield count


def contains_double_digits(password_str: str) -> bool:
    return any(map(lambda l: l == 2, matching_digit_group_lens(password_str)))


def valid_password2(password: int) -> bool:
    password_str = str(password)
    return len(password_str) == 6 and contains_double_digits(password_str) and no_decrease(password_str)


def problem1():
    return sum(map(valid_password1, range(307237, 769059)))


def problem2():
    return sum(map(valid_password2, range(307237, 769059)))


if __name__ == '__main__':
    print(problem1())
    print(problem2())
