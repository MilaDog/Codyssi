#!/usr/bin/env python


def reduce_line(line: str, use_hyphen: bool = True) -> str:
    """Reduce the line as much as possible."""
    has_changed: bool = False

    indx_to_remove: set[int] = set()
    for i in range(len(line) - 1):
        curr, nxt = line[i], line[i + 1]

        if i in indx_to_remove:
            continue

        if (curr.isdigit() and (nxt.isalpha() or (nxt == "-" and use_hyphen))) or (
            nxt.isdigit() and (curr.isalpha() or (curr == "-" and use_hyphen))
        ):
            has_changed = True
            indx_to_remove.add(i)
            indx_to_remove.add(i + 1)

    if has_changed:
        return reduce_line(
            line="".join(x for i, x in enumerate(line) if i not in indx_to_remove), use_hyphen=use_hyphen
        )
    return line


def solve() -> None:
    """Solve the problems."""
    use_example: bool = False

    sections: list[str] = open("day08.em" if use_example else "day08.in").read().split("\n")

    # Part 01
    p1: int = sum(sum(x.isalpha() for x in line) for line in sections)

    # Part 02
    p2: int = sum(len(reduce_line(line=line)) for line in sections)

    # Part 03
    p3: int = sum(len(reduce_line(line=line, use_hyphen=False)) for line in sections)

    print(f"Part 01: {p1}")
    print(f"Part 02: {p2}")
    print(f"Part 03: {p3}")


if __name__ == "__main__":
    solve()
