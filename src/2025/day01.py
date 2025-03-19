#!/usr/bin/env python

TEST_EXAMPLE: str = """8
1
5
5
7
6
5
4
3
1
-++-++-++"""


def calculate_result(values: list[int], instructions: list[str]) -> int:
    """Calculate the compass result."""
    res: int = 0
    for i, value in enumerate(values):
        if i == 0:
            res += value

        else:
            instruction: str = instructions[i - 1]
            if instruction == "+":
                res += value
            elif instruction == "-":
                res -= value

    return res


def solve() -> None:
    """Solve the problems."""
    # lines: list[str] = [line.strip() for line in TEST_EXAMPLE.splitlines()]
    lines: list[str] = [line.strip() for line in open("day01.in").readlines()]
    instructions: list[str] = list(lines[-1])
    values: list[int] = list(map(int, lines[:-1]))

    print(f"Part 01: {calculate_result(values=values, instructions=instructions)}")
    print(f"Part 02: {calculate_result(values=values, instructions=instructions[::-1])}")

    values_paired: list[int] = [values[i] * 10 + values[i + 1] for i in range(0, len(values), 2)]
    print(f"Part 03: {calculate_result(values=values_paired, instructions=instructions[::-1])}")


if __name__ == "__main__":
    solve()
