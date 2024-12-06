from pathlib import Path
from typing import List, Tuple

from aoc import PuzzleName, Dir


def get_next_indices(index_current: int,
                     index_min: int,
                     index_max: int) -> Tuple[int | None, int | None]:
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
        try:
            entry = matrix[y][x]
        except IndexError:
            break
        cross_section += entry
        x += vector[0]
        y -= vector[1]

    return cross_section


def process(lines: List[str],
            word: str = "XMAS") -> Tuple[List[str], int]:
    """
    Finds `word` occurrences in `lines`: horizontally, vertically, diagonally

    Args:
        lines: The lines of text to search in
        word: The word to look for

    Returns:
        Tuple[List of strings with only `word` characters, number of `word` occurrences]
    """
    lines_processed = []
    occurrence_count = 0

    for index_line, line in enumerate(lines):
        for index_char, char in enumerate(line):
            index_word = word.index(char)

            # Skip if character not in word
            if not 0 < index_word < len(word) - 1:
                continue
            print(char, index_word)

    return lines_processed, occurrence_count


def main(file_path: Path = None):
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

    processed_lines = process(lines)
    result = ""
    return result


if __name__ == "__main__":
    print(f"Result: {main()}")
