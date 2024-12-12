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
    Returns `vector` as a new vector, rotated by 90 degrees in `direction`

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
                return (index_x, index_y), get_vector(entry)


def get_vector(symbol: str) -> tuple[int, int]:
    """
    Returns a 2D vector given the `symbol`

    Args:
        symbol: One of `<,>,^,v` indicating the vector's direction

    Returns:
        [int, int] 2D vector
    """
    lookup_x_dir = {
        "<": -1,
        ">": +1,
    }
    lookup_y_dir = {
        "^": +1,
        "v": -1,
    }
    return (
        lookup_x_dir.get(symbol, 0),
        lookup_y_dir.get(symbol, 0),
    )


def get_entry(puzzle_input: list[list[str]], pos: tuple[int, int]):
    return puzzle_input[pos[1]][pos[0]]


def process(puzzle_input: list[list[str]]) -> list[tuple[int, int, str]]:
    """
    Returns the route that the guard walks - duplicate fields included

    Args:
        puzzle_input: The "room" the guard is walking in.

    Returns:
        A list of positions the guard visits in the puzzle_input
    """
    # Find initial guard position and vector
    pos, vec = get_guard(puzzle_input)
    guard_route: list[tuple[int, int, str]] = []

    while True:
        entry = get_entry(puzzle_input, pos)
        # Register position
        guard_route.append((pos[0], pos[1], entry))

        while True:
            # Get next step
            next_pos = (pos[0] + vec[0], pos[1] - vec[1])
            # Update vector when meeting an obstacle until it's clear ahead
            try:
                entry_next = get_entry(puzzle_input, next_pos)
            except IndexError:
                # Clear position to indicate it's off the map...
                pos = None
                break
            if entry_next == "#":
                vec = rotate(vec, 1)
            else:
                pos = next_pos
                break

        # ...stop when next field would be off the map
        if pos is None:
            break

    return guard_route


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
    visited = process(puzzle_input)
    distinct_visited = set(visited)
    return len(distinct_visited)


if __name__ == "__main__":
    RESULT = main()
    print(f"Result: {RESULT}")
