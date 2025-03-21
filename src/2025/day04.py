#!/usr/bin/env python
import re

TEST_EXAMPLE: str = """NNBUSSSSSDSSZZZZMMMMMMMM
PWAAASYBRRREEEEEEE
FBBOFFFKDDDDDDDDD
VJAANCPKKLZSSSSSSSSS
NNNNNNBBVVVVVVVVV"""


def calculate_value(line: str) -> int:
    """Calculat the storage value for the line."""
    return sum(abs(ord(c) - 64) if not c.isdigit() else int(c) for c in line)


def solve() -> None:
    """Solve the problems."""
    # data: list[str] = [x.strip() for x in TEST_EXAMPLE.splitlines()]
    data: list[str] = [x.strip() for x in open("day04.in").readlines()]

    p1: int = 0
    p2: int = 0
    p3: int = 0
    for line in data:
        p1 += calculate_value(line=line)

        offset: int = len(line) // 10
        new_line: str = line[:offset] + str(len(line[offset:-offset])) + line[-offset:]
        p2 += calculate_value(line=new_line)

        groups: list[str] = [str(len(x[0])) + x[0][0] for x in re.findall(r"((.)\2*)", line)]
        p3 += calculate_value(line="".join(groups))

    print(f"Part 01: {p1}")
    print(f"Part 02: {p2}")
    print(f"Part 03: {p3}")


if __name__ == "__main__":
    solve()
