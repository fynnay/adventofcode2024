from pathlib import Path

from aoc import (
    PuzzleName,
    Dir,
)


def get_input_values(file_path: Path):
    values = []

    with open(file_path, 'r') as file:
        for line in file.readlines():
            if not line:
                continue

    return values


def find_lowest_divisor(n: int, a: int, b: int, limit: int = 1000) -> tuple[int, int]:
    """
    Iteratively determines the lowest factors at which a combination of `a` and `b` fit into `n` up to `limit`.

    y = (n - a * x) / b

    Where `a` is min(a, b) and `b` is max(a, b)
    x starts at 0 and is gradually increased as long as y remains a non-negative integer.
    Continue iterating until `limit` is reached.

    Args:
        n: Goal
        a: Value 1 (the smaller of the two values)
        b: Value 2 (the larger of the two values)
        limit: Maximum number of iterations before giving up

    Returns:
        (a multiplier, b multiplier)
    """
    pass


def process(input_values):
    return None


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
