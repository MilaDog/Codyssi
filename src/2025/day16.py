#!/usr/bin/env python
from __future__ import annotations

import math
from copy import deepcopy


class Face:
    """Face of a dice."""

    def __init__(self, id_: int, size: int) -> None:
        self.id_: int = id_
        self.__size: int = size
        self.__grid: list[list[int]] = [[1 for _ in range(self.__size)] for _ in range(self.__size)]
        self.__absorption: int = 0

    def get_dominant_sum(self) -> int:
        """Get the dominant sum of the face."""
        return max(max(sum(row) for row in self.__grid), max(sum(col) for col in zip(*self.__grid)))

    def get_grid(self) -> list[list[int]]:
        """Get a copy of the grid."""
        return deepcopy(self.__grid)

    def get_absorption(self) -> int:
        """Get the absorption for the face."""
        return self.__absorption

    def rotate_clockwise(self) -> None:
        """Rotate the face clockwise."""
        self.__grid = [list(reversed(col)) for col in zip(*self.__grid)]

    def rotate_counter_clockwise(self) -> None:
        """Rotate the face counter-clockwise."""
        self.__grid = [list(row) for row in zip(*self.__grid[::-1])]

    def rotate_180(self) -> None:
        """Rotate the face 180 degrees."""
        self.rotate_clockwise()
        self.rotate_clockwise()

    @staticmethod
    def update_value(cell_value: int, value: int) -> int:
        """Update the value at the given position, ensuring it is between 1-100 inclusive."""
        return (cell_value + value - 1) % 100 + 1

    def update_face(self, value: int) -> None:
        """Update all the grid positions on the face."""
        self.__grid = [
            [self.update_value(cell_value=cell_value, value=value) for cell_value in row] for row in self.__grid
        ]

    def update_row(self, row: int, value: int) -> None:
        """Update all grid positions in the row on the face."""
        self.__grid[row] = [self.update_value(cell_value=cell_value, value=value) for cell_value in self.__grid[row]]

    def update_column(self, col: int, value: int) -> None:
        """Update all grid positions in the column on the face."""
        for row in self.__grid:
            row[col] = self.update_value(cell_value=row[col], value=value)

    def update_absorption(self, value: int) -> None:
        """Update the absorption of the face."""
        self.__absorption += value


class Cube:
    """Cube for the problem."""

    def __init__(self, face_size: int) -> None:
        self.__face_size: int = face_size

        # Format: FBLURD
        self.__faces: list[Face] = [Face(id_=i + 1, size=self.__face_size) for i in range(6)]
        self.__current: Face = self.__faces[0]
        self.__down: Face = self.__faces[1]
        self.__back: Face = self.__faces[2]
        self.__up: Face = self.__faces[3]
        self.__left: Face = self.__faces[4]
        self.__right: Face = self.__faces[5]

    def get_absorption(self) -> list[int]:
        """Get the dice absorptions."""
        return [f.get_absorption() for f in self.__faces]

    def perform_actions(self, instructions: list[str], twists: str, wrap: bool = False) -> None:
        """Perform each instruction with the twist."""
        for instruction, twist in zip(instructions, twists + " "):
            print(instruction, twist)
            self.__execute_instruction(instruction=instruction, wrap=wrap)
            self.__twist(twist=twist)

            for f in self.__faces:
                print(f"{f.id_}: ")
                print("\n".join(["\t".join([str(i) for i in row]) for row in f.get_grid()]))
                print()

    def __execute_instruction(self, instruction: str, wrap: bool) -> None:
        """Execute the given instruction on the current face."""
        parts: list[str] = instruction.replace("- VALUE ", "").split(" ")
        value: int = int(parts[-1])

        # Power
        power: int = value * (self.__face_size ** (1 + ("FACE" in parts)))
        self.__current.update_absorption(value=power)

        if parts[0] == "FACE":
            self.__current.update_face(value=value)

        elif parts[0] == "ROW":
            self.__current.update_row(row=int(parts[1]) - 1, value=value)

            if wrap:
                self.__right.update_row(row=int(parts[1]) - 1, value=value)
                self.__left.update_row(row=int(parts[1]) - 1, value=value)
                self.__back.rotate_180()
                self.__back.update_row(row=int(parts[1]) - 1, value=value)
                self.__back.rotate_180()

        elif parts[0] == "COL":
            self.__current.update_column(col=int(parts[1]) - 1, value=value)

            if wrap:
                self.__up.update_column(col=int(parts[1]) - 1, value=value)
                self.__down.update_column(col=int(parts[1]) - 1, value=value)
                self.__back.update_column(col=int(parts[1]) - 1, value=value)

        else:
            raise Exception("Invalid INSTRUCTION.")

    def __twist(self, twist: str) -> None:
        """Rotate the dice. Update the current faces and its neightbours."""
        # 0F 1B 2L 3U 4R 5D
        if twist == "L":
            # Face rotation
            self.__current, self.__left, self.__back, self.__right = (
                self.__left,
                self.__back,
                self.__right,
                self.__current,
            )

            # Grid rotation
            self.__up.rotate_counter_clockwise()
            self.__down.rotate_clockwise()
            # self.__back.rotate_180()
            # self.__left.rotate_180()

        elif twist == "U":
            # Face rotation
            self.__current, self.__up, self.__back, self.__down = self.__up, self.__back, self.__down, self.__current

            # Grid rotation
            self.__left.rotate_clockwise()
            self.__right.rotate_counter_clockwise()

        elif twist == "R":
            # Face rotation
            self.__current, self.__right, self.__back, self.__left = (
                self.__right,
                self.__back,
                self.__left,
                self.__current,
            )

            # Grid rotation
            self.__up.rotate_clockwise()
            self.__down.rotate_counter_clockwise()
            # self.__back.rotate_180()
            # self.__right.rotate_180()

        elif twist == "D":
            # Face rotation
            self.__current, self.__down, self.__back, self.__up = self.__down, self.__back, self.__up, self.__current

            # Grid rotation
            self.__left.rotate_counter_clockwise()
            self.__right.rotate_clockwise()

    def get_overall_dominant_sum(self) -> int:
        """Get the product of all the face's dominant sum."""
        return math.prod([f.get_dominant_sum() for f in self.__faces])


def part_01_02(size: int, instructions: list[str], twists: str) -> tuple[int, int]:
    """Solve Part 01 and 02."""
    cube: Cube = Cube(face_size=size)
    cube.perform_actions(instructions=instructions, twists=twists)
    return math.prod(sorted(cube.get_absorption())[-2:]), cube.get_overall_dominant_sum()


# def part_03(size: int, instructions: list[str], twists: str) -> int:
#     """Solve Part 03."""
#     cube: Cube = Cube(face_size=size)
#     cube.perform_actions(instructions=instructions, twists=twists, wrap=True)
#     return cube.get_overall_dominant_sum()


def solve() -> None:
    """Solve the problems."""
    use_example: bool = True
    file: str = "day16.em" if use_example else "day16.in"

    sections: list[str] = open(file).read().split("\n\n")
    twists: str = sections[-1]
    instructions: list[str] = sections[0].strip().split("\n")
    size: int = 3

    # Part 01, 02
    p1: int
    p2: int
    p1, p2 = part_01_02(instructions=instructions, twists=twists, size=size)

    # Part 03
    # p3: int = part_03(instructions=instructions, twists=twists, size=size)

    print(f"Part 01: {p1}")
    print(f"Part 02: {p2}")
    # print(f"Part 03: {p3}")


if __name__ == "__main__":
    solve()
