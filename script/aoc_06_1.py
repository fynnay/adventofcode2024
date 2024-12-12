"""
Predict the path of the guard. How many distinct positions will the guard visit before leaving the mapped area?
"""
from pathlib import Path

from aoc import (
    PuzzleName,
    Dir,
)


def rotate(vector: tuple[int, int], direction: 0 or 1) -> tuple[int, int]:
    """
    Returns new vector from rotating the specified one by 90 degrees

    Args:
        vector: The vector to be rotated
        direction: 0 for counterclockwise (left), 1 for clockwise (right)
    """
    new_vector = [vector[1], vector[0]]
    new_vector[direction] = -new_vector[direction]
    return new_vector[0], new_vector[1]


def get_puzzle_input(file_path: Path) -> list[list[str]]:
    values_y = []

    with open(file_path, 'r') as file:
        for line in file.readlines():
            if not line:
                continue
            values_x = []
            for entry in line:
                entry_sanitized = entry.strip("\n").strip("")
                if not entry_sanitized:
                    continue
                values_x.append(entry_sanitized)
            values_y.append(values_x)

    return values_y


def get_guard(puzzle_input: list[list[str]]) -> tuple[tuple[int, int], tuple[int, int]]:
    for index_y, line in enumerate(puzzle_input):
        for index_x, entry in enumerate(line):
            if entry in ["<", ">", "^", "v"]:
                return (index_x, index_y), get_dir(entry)


def get_dir(symbol: str) -> tuple[int, int]:
    lookup_x_dir = {
        "<": -1,
        ">": +1,
    }
    lookup_y_dir = {
        "^": -1,
        "v": +1,
    }
    return (
        lookup_x_dir.get(symbol, 0),
        lookup_y_dir.get(symbol, 0),
    )


def process(puzzle_input: list[list[str]]) -> int:
    guard_pos, guard_dir = get_guard(puzzle_input)

    max_y: int = len(puzzle_input)
    max_x: int = len(puzzle_input[0])
    visited: set[tuple[int, int]] = {guard_pos}
    steps: int = 0

    while True:
        guard_pos = (
            guard_pos[0] + guard_dir[0],
            guard_pos[1] + guard_dir[1],
        )
        x, y = guard_pos

        # Stop when guard exists
        if not 0 < x < max_x:
            break
        if not 0 < y < max_y:
            break

        # Change direction if meeting an obstacle
        entry = puzzle_input[y][x]
        if entry == "#":
            guard_dir = (_ for _ in guard_dir)


        steps += 1

        break

    return steps


def main(file_path: Path | None = None):
    script_path = Path(__file__)
    puzzle_name = PuzzleName.parse(script_path.stem)
    file_path = file_path or Dir.build_file_path(
        Dir.INPUT,
        puzzle_name=PuzzleName(
            day=puzzle_name.day,
            part=puzzle_name.part,
        )
    )

    puzzle_input = get_puzzle_input(file_path)
    result = process(puzzle_input)
    return result


if __name__ == "__main__":
    RESULT = main()
    print(f"Result: {RESULT}")
