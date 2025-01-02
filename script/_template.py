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
