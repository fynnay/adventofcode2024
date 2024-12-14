import itertools
from pathlib import Path
import math
from typing import Type, Callable

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


def multiply(a: float, b: float) -> float:
    return a * b


def add(a: float, b: float) -> float:
    return a + b


def get_combinations(locations: int, operators: list[any] = (multiply, add)) -> list[tuple[any, ...]]:
    """
    Returns lists of all possible combinations of operators with the given amount of locations
    """
    return list(itertools.product(operators, repeat=locations))


def validate(test: int, numbers: list[int]) -> bool:
    pass

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
