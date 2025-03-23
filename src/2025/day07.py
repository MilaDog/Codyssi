#!/usr/bin/env python
def solve() -> None:
    """Solve the problems."""
    use_example: bool = False

    sections: list[str] = open("day07.em" if use_example else "day07.in").read().split("\n\n")
    original_tracks: list[int] = list(map(int, sections[0].split("\n")))
    instructions: list[tuple[int, int]] = [(int(a), int(b)) for a, b in [x.split("-") for x in sections[1].split("\n")]]
    test_index: int = int(sections[-1])

    # Part 01
    tracks01: list[int] = original_tracks[::]
    for instruction in instructions:
        a, b = instruction
        tracks01[a - 1], tracks01[b - 1] = tracks01[b - 1], tracks01[a - 1]

    p1: int = tracks01[test_index - 1]

    # Part 02
    tracks02: list[int] = original_tracks[::]
    lngth: int = len(instructions)
    for i, instruction in enumerate(instructions):
        a, b = instruction
        c, _ = instructions[(i + 1) % lngth]
        tracks02[b - 1], tracks02[c - 1], tracks02[a - 1] = tracks02[a - 1], tracks02[b - 1], tracks02[c - 1]

    p2: int = tracks02[test_index - 1]

    # Part 03
    tracks03: list[int] = original_tracks[::]
    for instruction in instructions:
        a, b = instruction if instruction[0] < instruction[1] else instruction[::-1]
        block_a, block_b = tracks03[a - 1 : b - 1], tracks03[b - 1 :]

        min_lngth: int = min(len(block_a), len(block_b))
        for bi in range(min_lngth):
            # Swapping
            tracks03[a + bi - 1], tracks03[b + bi - 1] = tracks03[b + bi - 1], tracks03[a + bi - 1]

    p3: int = tracks03[test_index - 1]

    print(f"Part 01: {p1}")
    print(f"Part 02: {p2}")
    print(f"Part 03: {p3}")


if __name__ == "__main__":
    solve()
