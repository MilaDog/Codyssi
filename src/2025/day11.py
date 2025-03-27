#!/usr/bin/env python
import re


def get_value(c: str) -> int:
    """Get the integer value of the given character."""
    if c.isdigit():
        return int(c)

    if c.isupper():
        return ord(c) - 55

    if c.islower():
        return ord(c) - 61

    return 62 + "!@#$%^".index(c)


def encode_value(value: int) -> str:
    """Get the character for the given value."""
    if 0 <= value <= 9:
        return str(value)

    if 10 <= value <= 35:
        return chr(value + 55)

    if 36 <= value <= 61:
        return chr(value + 61)

    if 62 <= value <= 67:
        return "!@#$%^"[value - 62]

    return chr(value)


def convert_to_base_10(value: str, from_base: int) -> int:
    """Convert the given value from the given base into the base 10."""
    tlt: int = 0
    for i, c in enumerate(value[::-1]):
        tlt += (from_base**i) * get_value(c=c)

    return tlt


def convert_to_base(value: int, base: int) -> str:
    """Convert the given base-10 number to the given base."""
    res: str = ""

    while value > 0:
        res += encode_value(value=value % base)
        value //= base

    return res[::-1]


def get_smallest_base_having_given_length(value: int, length: int) -> int:
    """Get the smallest base that will have the converted `value` of the given `length`."""
    current_base: int = 11  # since we know that the given value, in the problem, does not have base-10 as the smallest.
    while True:
        res: str = convert_to_base(value=value, base=current_base)

        if len(res) <= length:
            return current_base

        current_base += 1


def solve() -> None:
    """Solve the problems."""
    use_example: bool = False
    lines: list[tuple[str, int]] = [
        (n, int(b)) for n, b in re.findall(r"(.+) (\d+)", open("day11.em" if use_example else "day11.in").read())
    ]

    # Part 01
    decimal_values: list[int] = [convert_to_base_10(value=number, from_base=base) for number, base in lines]
    p1: int = max(decimal_values)

    # Part 02
    p2: str = convert_to_base(value=sum(decimal_values), base=68)

    # Part 03
    p3: int = get_smallest_base_having_given_length(value=sum(decimal_values), length=4)

    print(f"Part 01: {p1}")
    print(f"Part 02: {p2}")
    print(f"Part 03: {p3}")


if __name__ == "__main__":
    solve()
