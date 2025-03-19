#!/usr/bin/env python

TEST_EXAMPLE: str = """912372
283723
294281
592382
721395
91238"""


def solve() -> None:
    """Solve the problems."""
    # data: list[int] = list(map(int, TEST_EXAMPLE.splitlines()))
    data: list[int] = list(map(int, open("./day01.in").readlines()))

    print(f"Part 01: {sum(data)}")

    p2: int = sum(sorted(data)[:-20])  # TEST_EXAMPLE uses [:-2]
    print(f"Part 02: {p2}")

    p3: int = sum(x if i % 2 == 0 else -x for i, x in enumerate(data))
    print(f"Part 03: {p3}")


if __name__ == "__main__":
    solve()
