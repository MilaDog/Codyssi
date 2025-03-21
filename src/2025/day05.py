#!/usr/bin/env python
import re
from collections import deque

TEST_EXAMPLE: str = """(-16, -191)
(92, 186)
(157, -75)
(39, -132)
(-42, 139)
(-74, -150)
(200, 197)
(-106, 105)"""


def manhatten_distance(start: tuple[int, int], destination: tuple[int, int]) -> int:
    """Manhatten distance from start to destination."""
    return abs(start[0] - destination[0]) + abs(start[1] - destination[1])


def solve() -> None:
    """Solve the problems."""
    # coords: list[tuple[int, int]] = [(int(x), int(y)) for x, y in re.findall(r"\((-?\d+), (-?\d+)\)", TEST_EXAMPLE)]
    coords: list[tuple[int, int]] = [
        (int(x), int(y)) for x, y in re.findall(r"\((-?\d+), (-?\d+)\)", open("day05.in").read())
    ]

    distance_coords: list[tuple[int, tuple[int, int]]] = sorted(
        [(manhatten_distance(start=(0, 0), destination=d), d) for d in coords], key=lambda x: x[0]
    )

    p1: int = distance_coords[-1][0] - distance_coords[0][0]
    p2: int = sorted([manhatten_distance(start=distance_coords[0][1], destination=x[1]) for x in distance_coords[1:]])[
        0
    ]

    unvisited: deque[tuple[int, int]] = deque(coords[::])
    start: tuple[int, int] = (0, 0)
    p3: int = 0

    while unvisited:
        res: list[tuple[int, tuple[int, int]]] = sorted(
            [(manhatten_distance(start=start, destination=d), d) for d in unvisited],
            key=lambda x: (x[0], x[1][0], x[1][1]),
        )
        p3 += res[0][0]
        start = res[0][1]
        unvisited.remove(start)

    print(f"Part 01: {p1}")
    print(f"Part 02: {p2}")
    print(f"Part 03: {p3}")


if __name__ == "__main__":
    solve()
