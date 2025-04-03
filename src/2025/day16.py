#!/usr/bin/env python
from __future__ import annotations

import math
from dataclasses import dataclass, field


@dataclass
class Face:
    """Face of a dice."""
    
    id_: int = field()
    values: list[list[int]] = field()

    def dominant_sum(self) -> int:
        """Get the dominant sum of the face."""
        return max(
            max(sum(row) for row in self.values),
            max(sum(col) for col in zip(*self.values))
        )

    def rotate_clockwise(self) -> None:
        """Rotate the face clockwise."""
        self.values = [list(reversed(col)) for col in zip(*self.values)]

    def rotate_counter_clockwise(self) -> None:
        """Rotate the face counter-clockwise."""
        self.values = list(list(col) for col in zip(*self.values))[::-1]


class Dice:
    """Dice for the problem."""
    def __init__(self, face_size: int) -> None:
        self.__face_size: int = face_size

        # Format: FBLURD
        self.__faces: list[Face] = self.__create_dice()

        # Dice absorption
        self.__absorption: dict[int, int] = {i+1:0 for i in range(6)}


    def __create_dice(self) -> list[Face]:
        """Create the Faces of the Dice. Returns in the order: FBLURD"""
        faces: list[Face] = []

        for i in range(6):
            faces.append(Face(id_=i+1, values=[[1 for _ in range(self.__face_size)] for _ in range(self.__face_size)]))

        return [faces[0], faces[2], faces[4], faces[3], faces[5], faces[1]]

    def get_face(self) -> Face:
        """Get the current face; the one in front."""
        return self.__faces[0]

    def get_faces(self) -> list[Face]:
        """Get all the faces."""
        return self.__faces

    def get_absorption(self) -> dict[int, int]:
        """Get the dice absorptions."""
        return self.__absorption

    def perform_actions(self, instructions: list[str], twists: str) -> None:
        """Perform each instruction with the twist."""
        for instruction, twist in zip(instructions, twists + " "):
            self.perform_action(instruction=instruction, twist=twist)

    def perform_action(self, instruction: str, twist: str) -> None:
        """Perform the giving instruction, and then the twist afterwards."""
        self.__calculate_instruction_power(instruction=instruction)
        self.__execute_instruction(instruction=instruction)
        self.__twist(twist=twist)

    def __calculate_instruction_power(self, instruction: str) -> None:
        """Determine the power of the instruction. Add it to the overall dice absorption."""
        parts: list[str] = instruction.replace("- VALUE ", "").split(" ")

        power: int = int(parts[-1]) * self.__face_size * (self.__face_size ** ("FACE" in parts))
        self.__absorption[self.__faces[0].id_] += power

    def __execute_instruction(self, instruction: str) -> None:
        """Execute the given instruction on the current face."""
        parts: list[str] = instruction.replace("- VALUE ", "").split(" ")

        current_face: Face = self.__faces[0]
        val: int = 0
        if parts[0] == "FACE":
            for x in range(self.__face_size):
                for y in range(self.__face_size):
                    val = current_face.values[x][y] + int(parts[-1])
                    current_face.values[x][y] = val if val <= 100 else val % 100

        elif parts[0] == "ROW":
            r: int = int(parts[1]) - 1
            for y in range(self.__face_size):
                val = current_face.values[r][y] + int(parts[-1])
                current_face.values[r][y] = val if val <= 100 else val % 100

        elif parts[0] == "COL":
            c: int = int(parts[1]) - 1
            for x in range(self.__face_size):
                val = current_face.values[x][c] + int(parts[-1])
                current_face.values[x][c] = val if val <= 100 else val % 100
        
        else:
            raise Exception("Invalid INSTRUCTION.")


    def __twist(self, twist: str) -> None:
        """Rotate the dice. Update the current faces and its neightbours."""
        if twist == " ":
            return

        face_f, face_b, face_l, face_u, face_r, face_d = self.__faces

        # FBLURD
        if twist == "R":
            self.__faces = [face_r, face_l, face_f, face_u, face_b, face_d]
            face_d.rotate_clockwise()
            face_u.rotate_clockwise()

        elif twist == "D":
            self.__faces = [face_d, face_u, face_l, face_f, face_r, face_b]
            face_l.rotate_counter_clockwise()
            face_r.rotate_counter_clockwise()

        elif twist == "L":
            self.__faces = [face_l, face_r, face_b, face_u, face_f, face_d]
            face_d.rotate_counter_clockwise()
            face_u.rotate_counter_clockwise()

        elif twist == "U":
            self.__faces = [face_u, face_d, face_l, face_b, face_r, face_f]
            face_l.rotate_clockwise()
            face_r.rotate_clockwise()

        else:
            raise Exception("Invalid TWIST.")

    def get_dominant_sum(self) -> int:
        """Determine the dominant sum of each face, and return the product of them all."""
        sums: list[int] = [face.dominant_sum() for face in self.__faces]
        return math.prod(sums)


def solve() -> None:
    """Solve the problems."""
    use_example: bool = False
    file: str = "day16.em" if use_example else "day16.in"

    sections: list[str] = open(file).read().split("\n\n")
    twists: str = sections[-1]
    instructions: list[str] = sections[0].strip().split("\n")

    dice: Dice = Dice(face_size=80)
    dice.perform_actions(instructions=instructions, twists=twists)

    # Part 01
    p1: int = math.prod(sorted(dice.get_absorption().values())[-2:])

    # Part 02
    p2: int = dice.get_dominant_sum()

    # Part 03
    p3: int = 0

    print(f"Part 01: {p1}")
    print(f"Part 02: {p2}")
    print(f"Part 03: {p3}")


if __name__ == "__main__":
    solve()
