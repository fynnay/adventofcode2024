import itertools
from pathlib import Path
import math
from typing import Type, Callable

from aoc import (
    PuzzleName,
    Dir,
)


INPUT_VALUE = tuple[int, list[int]]
INPUT_VALUES = list[INPUT_VALUE]


def get_input_values(file_path: Path) -> INPUT_VALUES:
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
    Returns lists of all possible combinations of operators given the amount of locations
    """
    return list(itertools.product(operators, repeat=locations))


def validate(input_value: INPUT_VALUE) -> bool:
    test, numbers = input_value
    operator_combinations = get_combinations(len(numbers) - 1, [multiply, add])

    operators: list[Callable]
    for operators in operator_combinations:
        result = None
        for index, number in enumerate(numbers):
            if result is None:
                result = number
                continue
            a = result
            b = number
            operator = operators[index - 1]
            result = operator(a, b)
        if result == test:
            return True

    return False

def process(input_values: INPUT_VALUES) -> list[bool]:
    results = []
    for input_value in input_values:
        is_valid = validate(input_value)
        results.append(is_valid)
    return results



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
