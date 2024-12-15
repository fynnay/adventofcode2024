"""
The signal only applies its nefarious effect at specific antinodes based on the resonant frequencies of the antennas.
In particular, an antinode occurs at any point that is perfectly in line with two antennas of the same frequency -
but only when one of the antennas is twice as far away as the other. This means that for any pair of antennas with
the same frequency, there are two antinodes, one on either side of them.

Antennas with different frequencies don't create antinodes; A and a count as different frequencies.
However, antinodes can occur at locations that contain antennas.


"""
from pathlib import Path

from aoc import (
    PuzzleName,
    Dir,
)


# Custom Types
POINT = tuple[int, int]
VECTOR = tuple[int, int]
MATRIX = list[list[str]]


def get_input_values(file_path: Path) -> MATRIX:
    values = []

    with open(file_path, 'r') as file:
        for line in file.readlines():
            if not line:
                continue
            entries = [_ for _ in line.strip("\n").strip(" ")]
            values.append(entries)

    return values

def show_matrix(
        matrix: MATRIX,
):
    for line in matrix:
        print("".join(line))

def get_cross_section(
        matrix: MATRIX,
        point: POINT,
        vector: VECTOR,
        length: int = None,
) -> list[tuple[tuple[int, int], str]]:
    """
    Returns a cross-section from the `matrix` at the `point` in the direction of the `vector`.
    If length is specified, limit the amount of returned points
    """
    x, y = point
    vx, vy = vector
    cross_section = []

    for _ in range(length):
        if x < 0 or y < 0:
            break
        try:
            entry = matrix[y][x]
        except IndexError:
            break
        x += vx
        y += vy
        cross_section += entry

    return cross_section


def process(input_values):
    show_matrix(input_values)
    return input_values


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
    input_values = get_input_values(file_path)
    result = process(input_values)
    return result


if __name__ == "__main__":
    RESULT = main()
    print(f"Result: {RESULT}")
