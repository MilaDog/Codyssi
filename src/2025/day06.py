#!/usr/bin/env python
import re
import string

TEST_EXAMPLE: str = (
    """t#UD$%%DVd*L?^p?S$^@#@@$pF$?xYJ$LLv$@%EXO&$*iSFZuT!^VMHy#zKISHaBj?e*#&yRVdemc#?&#Q%j&ev*#YWRi@?mNQ@eK"""
)


def solve() -> None:
    """Solve the problems."""
    # data = TEST_EXAMPLE
    data: str = open("day06.in").read()

    chars: list[str] = list(re.findall(r"[a-zA-Z]", data))

    # not very efficient, just still. Fun way to do it
    letters: str = f" {string.ascii_lowercase}{string.ascii_uppercase}"

    p1: int = len(chars)
    p2: int = sum(letters.index(c) for c in chars)
    p3: int = 0

    prev_c_val: int = 0
    for c in data:
        if c not in letters:
            # Determine value
            corrupt_val: int = (prev_c_val * 2) - 5

            if corrupt_val < 1:
                while corrupt_val < 1:
                    corrupt_val += 52

            elif corrupt_val > 52:
                while corrupt_val > 52:
                    corrupt_val -= 52

            prev_c_val = corrupt_val
            p3 += corrupt_val
            continue

        c_val: int = letters.index(c)
        p3 += c_val
        prev_c_val = c_val

    print(f"Part 01: {p1}")
    print(f"Part 02: {p2}")
    print(f"Part 03: {p3}")


if __name__ == "__main__":
    solve()
