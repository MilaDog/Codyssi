#!/usr/bin/env python
from collections import deque
from copy import deepcopy


def display_grid(grid: dict[tuple[int, int], int], size: int) -> None:
    """Display the grid."""
    for x in range(size):
        for y in range(size):
            print(grid[(x, y)], end="\t")
        print()


def do_all(grid: dict[tuple[int, int], int], amount: int, type_: str) -> None:
    """Do the `ALL` instruction on the grid."""
    for k in grid.keys():
        if type_ == "ADD":
            grid[k] += amount

        elif type_ == "SUB":
            grid[k] -= amount

        elif type_ == "MULTIPLY":
            grid[k] *= amount

        else:
            assert "Invalid INSTRUCTION type."

        # Overflow
        grid[k] = grid[k] % 1073741824


def do_shift(grid: dict[tuple[int, int], int], size: int, type_: str, row_col_number: int, shift_amount: int) -> None:
    """Perform the `SHIFT` instruction on the grid."""
    if type_ == "ROW":
        row_values: list[int] = [grid[row_col_number - 1, i] for i in range(size)]
        shifted_row_values: deque[int] = deque(row_values)
        shifted_row_values.rotate(shift_amount)

        # Adding back into grid
        for i, v in enumerate(shifted_row_values):
            grid[(row_col_number - 1, i)] = v

    elif type_ == "COL":
        col_values: list[int] = [grid[i, row_col_number - 1] for i in range(size)]
        shifted_col_values: deque[int] = deque(col_values)
        shifted_col_values.rotate(shift_amount)

        # Adding back into grid
        for i, v in enumerate(shifted_col_values):
            grid[(i, row_col_number - 1)] = v

    else:
        assert "Invalid SHIFT type."


def do_row_col_action(
    grid: dict[tuple[int, int], int], amount: int, type_: str, size: int, is_row: bool, row_col: int
) -> None:
    """Do the instruction on the given ROW/COL."""
    for i in range(size):
        position: tuple[int, int] = (int(row_col) - 1, i) if is_row else (i, int(row_col) - 1)

        if type_ == "ADD":
            grid[position] += int(amount)

        elif type_ == "SUB":
            grid[position] -= int(amount)

        elif type_ == "MULTIPLY":
            grid[position] *= int(amount)

        else:
            assert "Invalid INSTRUCTION type."

        # Overflow
        grid[position] = grid[position] % 1073741824


def do_instruction(instruction: list[str], grid: dict[tuple[int, int], int], size: int) -> None:
    """Perform the given instruction on the ROW/COL in the grid."""
    # Instruction action on
    if "ALL" in instruction:
        # Perform on all values in the grid
        instr: str = instruction[0]
        amount: int = int(instruction[1])

        do_all(grid=grid, amount=amount, type_=instr)

    elif "SHIFT" in instruction:
        # Performing a SHIFT
        type_: str = instruction[1]
        number: int = int(instruction[2])
        amount: int = int(instruction[-1])

        do_shift(grid=grid, size=size, type_=type_, row_col_number=number, shift_amount=amount)

    else:
        # Perform on the given ROW/COL
        instr: str = instruction[0]
        amount: int = int(instruction[1])
        is_row: bool = instruction[2] == "ROW"
        row_col: int = int(instruction[-1])

        do_row_col_action(grid=grid, amount=amount, size=size, type_=instr, is_row=is_row, row_col=row_col)


def get_highest_row_col_sum(grid: dict[tuple[int, int], int], size: int) -> int:
    """Get the highest sum of the ROWS/COLS."""
    row_col_sum_values: list[int] = []

    for i in range(size):
        row: int = 0
        col: int = 0

        for j in range(size):
            row += grid[(i, j)]
            col += grid[(j, i)]

        row_col_sum_values.append(row)
        row_col_sum_values.append(col)

    return max(row_col_sum_values)


def do_actions(
    grid: dict[tuple[int, int], int],
    size: int,
    actions: list[str],
    instructions: list[list[str]],
    exhaust: bool = False,
) -> None:
    """Perform all the ACTIONs on the instruction set."""
    dq_actions: deque[str] = deque(actions)
    dq_instructions: deque[list[str]] = deque(instructions)

    instruction: list[str] = []
    while dq_actions:
        if exhaust and not dq_instructions and not instruction:
            break

        curr: str = dq_actions.popleft()

        if curr == "TAKE":
            instruction = dq_instructions.popleft()

        elif curr == "CYCLE":
            dq_instructions.append(instruction)

        elif curr == "ACT":
            # Perform the action.
            do_instruction(instruction=instruction, grid=grid, size=size)
            instruction = []

        else:
            assert "Invalid ACTION type."

        # Part 03
        if exhaust:
            dq_actions.append(curr)


def part_01(grid: dict[tuple[int, int], int], size: int, instructions: list[list[str]]) -> int:
    """Solve Part 01 of the problem."""
    for instruction in instructions:
        do_instruction(instruction=instruction, grid=grid, size=size)

    return get_highest_row_col_sum(grid=grid, size=size)


def part_02(grid: dict[tuple[int, int], int], size: int, instructions: list[list[str]], actions: list[str]) -> int:
    """Solve Part 02 of the problem."""
    do_actions(grid=grid, size=size, instructions=instructions, actions=actions)
    return get_highest_row_col_sum(grid=grid, size=size)


def part_03(grid: dict[tuple[int, int], int], size: int, instructions: list[list[str]], actions: list[str]) -> int:
    """Solve Part 03 of the problem."""
    do_actions(grid=grid, size=size, instructions=instructions, actions=actions, exhaust=True)
    return get_highest_row_col_sum(grid=grid, size=size)


def solve() -> None:
    """Solve the problems."""
    use_example: bool = False
    file: str = "day12.em" if use_example else "day12.in"

    size: int = 30 if not use_example else 5

    sections: list[str] = open(file).read().strip().split("\n\n")

    grid_values: list[list[str]] = [line.strip().split(" ") for line in sections[0].split("\n")]
    grid_original: dict[tuple[int, int], int] = {
        (x, y): int(grid_values[x][y]) for x in range(size) for y in range(size)
    }

    instructions: list[list[str]] = [line.strip().split(" ") for line in sections[1].split("\n")]

    flow_controls: list[str] = [x.strip() for x in sections[-1].strip().split("\n")]

    # Part 01
    p1: int = part_01(grid=deepcopy(grid_original), instructions=instructions, size=size)

    # Part 02
    p2: int = part_02(grid=deepcopy(grid_original), actions=flow_controls, instructions=instructions, size=size)

    # Part 03
    p3: int = part_03(grid=deepcopy(grid_original), actions=flow_controls, instructions=instructions, size=size)

    print(f"Part 01: {p1}")
    print(f"Part 02: {p2}")
    print(f"Part 03: {p3}")


if __name__ == "__main__":
    solve()
