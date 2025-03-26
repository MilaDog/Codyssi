#!/usr/bin/env python
import heapq
import math


def find_shortest_path(
    grid: dict[tuple[int, int], int], start: tuple[int, int], target: tuple[int, int], size: int = 20
) -> int:
    """In the grid, find the shortest path from `start` to `target`."""
    shortest_path: float = math.inf
    directions: list[tuple[int, int]] = [(0, 1), (1, 0)]  # RIGHT, DOWN
    q: list[tuple[int, tuple[int, int]]] = [(grid[start], start)]
    seen: set[tuple[int, int]] = set()

    while q:
        curr_pos: tuple[int, int]
        path_danger: int
        path_danger, curr_pos = heapq.heappop(q)

        # If target, end
        if curr_pos == target and path_danger < shortest_path:
            shortest_path = path_danger
            continue

        # Not seen
        if curr_pos not in seen:
            seen.add(curr_pos)

            # Directions
            for dirr in directions:
                dx, dy = curr_pos[0] + dirr[0], curr_pos[1] + dirr[1]

                # Within grid bounds
                if 0 <= dx < size and 0 <= dy < size:
                    new_direction: tuple[int, int] = (dx, dy)
                    to_process: tuple[int, tuple[int, int]] = (path_danger + grid[new_direction], new_direction)
                    heapq.heappush(q, to_process)

    return int(shortest_path)


def solve() -> None:
    """Solve the problems."""
    use_example: bool = False
    size: int = 20 if use_example else 50

    rows: list[list[int]] = [
        list(map(int, line.strip().split(" "))) for line in open("day10.em" if use_example else "day10.in").readlines()
    ]
    cols: list[list[int]] = [list(col) for col in zip(*rows)]
    grid: dict[tuple[int, int], int] = {(x, y): rows[x][y] for x in range(size) for y in range(size)}

    # Part 01
    p1: int = min(sum(v) for v in [*rows, *cols])

    # Part 02
    p2: int = find_shortest_path(grid=grid, start=(0, 0), target=(14, 14))

    # Part 03
    p3: int = find_shortest_path(grid=grid, start=(0, 0), target=(size - 1, size - 1), size=size)

    print(f"Part 01: {p1}")
    print(f"Part 02: {int(p2)}")
    print(f"Part 03: {p3}")


if __name__ == "__main__":
    solve()
