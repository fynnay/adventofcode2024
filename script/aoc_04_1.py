from enum import Flag, IntFlag, IntEnum, Enum
from pathlib import Path
from typing import List, Tuple

from aoc import PuzzleName, Dir


def get_next_indices(
        index_current: int,
        index_min: int,
        index_max: int
) -> Tuple[int | None, int | None]:
    """
    Returns previous and next index given a range
    Args:
        index_current:
        index_min:
        index_max:

    Returns:

    """
    index_previous = index_current - 1
    if index_previous < index_min:
        index_previous = None

    index_next = index_current + 1
    if index_next > index_max:
        index_next = None

    return index_previous, index_next


def get_cross_section(
        matrix: List[str],
        pos: Tuple[int, int],
        vector: Tuple[int, int],
        length: int
) -> str:
    cross_section = ""
    x, y = pos

    for _ in range(length):
        if x < 0 or y < 0:
            break
        try:
            entry = matrix[y][x]
        except IndexError:
            break
        x += vector[0]
        y += vector[1]
        cross_section += entry

    return cross_section


class VECTOR(Enum):
    HORIZONTAL = (1, 0)
    VERTICAL = (0, 1)
    DIAGONAL_RIGHT = (1, 1)
    DIAGONAL_LEFT = (-1, 1)


def get_cross_sections(matrix: List[str], pos: Tuple[int, int], length: int) -> List[str]:
    cross_sections = []
    for vector in VECTOR:
        cross_section = get_cross_section(
            matrix,
            pos,
            vector.value,
            length,
        )
        if len(cross_section) < length:
            continue
        cross_sections.append(cross_section)

    return cross_sections


def count_occurrences(
        lines: List[str],
        word: str = "XMAS"
) -> int:
    """
    Finds `word` occurrences in `lines`: horizontally, vertically, diagonally, forwards and backwards

    Args:
        lines: The lines of text to search in
        word: The word to look for

    Returns:
        Tuple[List of strings with only `word` characters, number of `word` occurrences]
    """
    lines_processed = []
    occurrences = 0

    for vector in VECTOR:
        print(f"vec: {vector}")
        for index_line, line in enumerate(lines):
            for index_char, char in enumerate(line):
                cross_section = get_cross_section(
                    lines,
                    (index_char, index_line),
                    vector.value,
                    len(word),
                )
                if cross_section in [word, word[::-1]]:
                    occurrences += 1

    return occurrences


def main(
        file_path: Path = None
        ):
    script_path = Path(__file__)
    puzzle_name = PuzzleName.parse(script_path.stem)
    file_path = file_path or Dir.build_file_path(
        Dir.INPUT,
        puzzle_name=PuzzleName(
            day=puzzle_name.day,
            part=puzzle_name.part,
        )
    )

    with open(file_path, 'r') as fil:
        lines = fil.readlines()

    occurrences = count_occurrences(lines)
    return occurrences


if __name__ == "__main__":
    print(f"Result: {main()}")
