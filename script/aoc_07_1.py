import itertools
from pathlib import Path
from typing import Callable

from aoc import (
    PuzzleName,
    Dir,
)

INPUT_VALUE = tuple[int, list[int]]
INPUT_VALUES = list[INPUT_VALUE]
OPERATOR = Callable


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


def get_combinations(items: tuple[any], location_count: int) -> list[tuple]:
    """
    Returns lists of all possible combinations of items given the amount of locations
    """
    return list(itertools.product(items, repeat=location_count))


def apply_operators(operators: tuple[OPERATOR], numbers: list[float]) -> float:
    """
    Returns the result of applying the operators to the numbers
    """
    result = None

    for index, number in enumerate(numbers):
        if result is None:
            result = number
            continue

        a = result
        b = number
        operator = operators[index - 1]
        result = operator(a, b)

    return result


def get_valid_operator_combination(input_value: INPUT_VALUE, operators: tuple[Callable]=(multiply, add,)) -> tuple[OPERATOR] or None:
    """
    Returns a list of operators that, when applied to the numbers in the given order, will produce the given test value
    """
    test, numbers = input_value
    operator_combinations = get_combinations(operators, len(numbers) - 1)

    for op_combo in operator_combinations:
        result = apply_operators(op_combo, numbers)
        if result == test:
            return op_combo

    return None


def filter_input_values(input_values: INPUT_VALUES) -> list[tuple[INPUT_VALUE, list[Callable]]]:
    """
    Returns a list of input values and a list of valid operators
    """
    results = []

    for input_value in input_values:
        operators = get_valid_operator_combination(input_value)
        if not operators:
            continue
        results.append((input_value, operators))

    return results


def process(input_values: INPUT_VALUES) -> int:
    """
    Returns the SUM of all valid test values
    """
    results = []
    valid_input_values = filter_input_values(input_values)

    for input_value, operators in valid_input_values:
        test, numbers = input_value
        # NOTE: Optionally you can apply the operators again to double-check it matches the test
        # result = apply_operators(operators, numbers)
        results.append(test)

    return sum(results)


def main(file_path: Path | None = None):
    # Read input file
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
