#!/usr/bin/env python
import math
from collections import defaultdict, deque


def get_product_highest_three_shortest_paths(
    location_map: dict[str, list[tuple[str, int]]], use_values: bool = False
) -> int:
    """Solve Part 01."""
    # Simply traversing problem, keeping track of the path that has been taken.
    seen: set[str] = set()
    all_paths: list[int] = []

    q: deque[tuple[str, int]] = deque([("STT", 0)])

    while q:
        pos, lngth = q.popleft()

        if pos not in seen:
            seen.add(pos)
            all_paths.append(lngth)

            for nxt, value in location_map[pos]:
                q.append((nxt, lngth + (value**use_values)))

    return math.prod(sorted(all_paths)[-3:])


def get_longest_cycle(location_map: dict[str, list[tuple[str, int]]]) -> int:
    """Determine the longest cycle. Locations can only be visited once."""
    unique_locations: set[str] = set(location_map.keys())

    for nxt in location_map.values():
        for x, _ in nxt:
            unique_locations.add(x)

    all_paths: list[int] = []

    for start in unique_locations:
        # Go through each new location and determine if it is cycle
        seen: set[str] = set()

        q: deque[tuple[str, int]] = deque([(start, 0)])

        while q:
            pos, lngth = q.popleft()

            # Checking if valid
            if pos == start and start in seen:
                # Valid path
                all_paths.append(lngth)
                continue

            if pos not in seen:
                seen.add(pos)

                for nxt, value in location_map[pos]:
                    q.append((nxt, lngth + value))

    return max(all_paths)


def solve() -> None:
    """Solve the problems."""
    use_example: bool = False
    file: str = "day13.em" if use_example else "day13.in"

    data: list[list[str]] = [
        line.strip().replace(" -> ", " ").replace(" | ", " ").split() for line in open(file).readlines()
    ]

    location_map: dict[str, list[tuple[str, int]]] = defaultdict(list)
    for start, end, value in data:
        location_map[start].append((end, int(value)))

    # Part 01
    p1: int = get_product_highest_three_shortest_paths(location_map=location_map)

    # Part 02
    p2: int = get_product_highest_three_shortest_paths(location_map=location_map, use_values=True)

    # Part 03
    p3: int = get_longest_cycle(location_map=location_map)

    print(f"Part 01: {p1}")
    print(f"Part 02: {p2}")
    print(f"Part 03: {p3}")


if __name__ == "__main__":
    solve()
