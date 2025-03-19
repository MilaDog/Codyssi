#!/usr/bin/env python
import re

TEST_EXAMPLE: str = """8-9 9-10
7-8 8-10
9-10 5-10
3-10 9-10
4-8 7-9
9-10 2-7"""


def solve() -> None:
    """Solve the problems."""
    data: str = open("day03.in").read()

    values: list[list[int]] = [list(map(int, re.findall(r"\d+", line))) for line in re.findall(r"\d+-\d+", data)]

    p1: int = sum(b - a + 1 for a, b in values)
    print(f"Part 01: {p1}")

    p2: int = 0
    for i in range(0, len(values), 2):
        a, b = values[i]
        aa, bb = values[i + 1]

        p2 += len(set(list(range(a, b + 1)) + list(range(aa, bb + 1))))

    print(f"Part 02: {p2}")

    p3: list[int] = []
    for i in range(0, len(values), 2):
        boxes: set[int] = set()

        for box in values[i : i + 4]:
            boxes.update(list(range(box[0], box[1] + 1)))

        p3.append(len(boxes))

    print(f"Part 03: {max(p3)}")


if __name__ == "__main__":
    solve()
