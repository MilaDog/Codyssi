#!/usr/bin/env python
import re
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Item:
    """Item in the file."""

    id_: int = field()
    name: str = field()
    quality: int = field()
    cost: int = field()
    materials: int = field()


def max_items_value(items: list[Item], cost_target: int) -> int:
    """Simple DP approach to finding the combination of Items that reach the target goal."""
    # Processing
    dp: list[Any] = [None for _ in range(cost_target + 1)]
    dp[0] = (0, 0)

    for item in items:
        for total_cost in range(cost_target, -1, -1):
            if total_cost + item.cost <= cost_target and dp[total_cost] is not None:
                curr_quality, curr_materials = dp[total_cost]
                new_value: tuple[int, int] = (curr_quality + item.quality, curr_materials + item.materials)

                if dp[total_cost + item.cost] is None:
                    dp[total_cost + item.cost] = new_value
                else:
                    dp[total_cost + item.cost] = max(dp[total_cost + item.cost], new_value)

    best_choice: tuple[int, int] | None = None

    for i in range(cost_target + 1):
        if dp[i] is not None and (best_choice is None or dp[i] > best_choice):
            best_choice = dp[i]

    return best_choice[0] * best_choice[1] if best_choice is not None else -1


def solve() -> None:
    """Solve the problems."""
    use_example: bool = False
    file: str = "day14.em" if use_example else "day14.in"

    # Format: 1 ETdhCGi | Quality : 36, Cost : 25, Unique Materials : 7
    data: list[list[str]] = re.findall(
        r"(\d+) ([a-zA-Z]+) \| Quality : (\d+), Cost : (\d+), Unique Materials : (\d+)", open(file).read()
    )

    # Items
    items: list[Item] = [
        Item(id_=int(x[0]), name=x[1], quality=int(x[2]), cost=int(x[3]), materials=int(x[4])) for x in data
    ]

    # Part 01
    p1: int = sum(x.materials for x in sorted(items, key=lambda x: (x.quality, x.cost))[-5:])

    # Part 02
    p2: int = max_items_value(items=items, cost_target=30)

    # Part 03
    p3: int = max_items_value(items=items, cost_target=300)

    print(f"Part 01: {p1}")
    print(f"Part 02: {p2}")
    print(f"Part 03: {p3}")


if __name__ == "__main__":
    solve()
