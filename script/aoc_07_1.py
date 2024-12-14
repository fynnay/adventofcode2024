from pathlib import Path
from typing import Type

from aoc import (
    PuzzleName,
    Dir,
)


INPUT_VALUE = tuple[int, list[int]]


def get_input_values(file_path: Path) -> list[INPUT_VALUE]:
    values = []

    with open(file_path, 'r') as file:
        for line in file.readlines():
            if not line:
                continue
            test, numbers = line.split(":")
            test_int = int(test.strip(" "))
            numbers_int = [int(_) for _ in numbers.split(" ") if _]
            values.append((test_int, numbers_int))

    return values


def process():
    pass


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
    result = input_values
    return result


if __name__ == "__main__":
    RESULT = main()
    print(f"Result: {RESULT}")
