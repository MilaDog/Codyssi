#!/usr/bin/env python
import re

TEST_EXAMPLE: str = """Function A: ADD 495
Function B: MULTIPLY 55
Function C: RAISE TO THE POWER OF 3

5219
8933
3271
7128
9596
9407
7005
1607
4084
4525
5496"""


def calculate_result(median_room: int, functions: list[int]) -> int:
    """Calculate the room price."""
    assert len(functions) == 3

    for i, f in enumerate(functions):
        if i == 0:
            median_room **= f

        elif i == 1:
            median_room *= f

        else:
            median_room += f

    return median_room


def solve() -> None:
    """Solve the problems."""
    # values: list[int] = list(map(int, re.findall(r"\d+", TEST_EXAMPLE)))
    values: list[int] = list(map(int, re.findall(r"\d+", open("day02.in").read())))

    functions, rooms = values[:3][::-1], values[3:]

    median_room: int = list(sorted(values))[len(values) // 2]
    print(f"Part 01: {calculate_result(median_room=median_room, functions=functions)}")

    sum_even_rooms: int = sum(filter(lambda x: x % 2 == 0, rooms))
    print(f"Part 02: {calculate_result(median_room=sum_even_rooms, functions=functions)}")

    rooms_values: list[tuple[int, int]] = [
        (i, calculate_result(median_room=x, functions=functions)) for i, x in enumerate(rooms)
    ]
    best_valued_room: int = max(filter(lambda x: x[1] <= 15000000000000, rooms_values), key=lambda x: x[1])[0]
    print(f"Part 03: {rooms[best_valued_room]}")


if __name__ == "__main__":
    solve()
