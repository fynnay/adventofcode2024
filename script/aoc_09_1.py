from pathlib import Path

from aoc import (
    PuzzleName,
    Dir,
)


def get_input_values(file_path: Path) -> list[str]:
    values = []

    with open(file_path, 'r') as file:
        for line in file.readlines():
            if not line:
                continue
            values += [_ for _ in line if _]

    return values


def unpack(input_values: list[str]) -> list[str]:
    unpacked_values: list[str] = []

    for index, _ in enumerate(input_values):
        uid = int(index / 2)
        is_free = (index + 1) % 2 == 0
        if is_free:
            value = "."
        else:
            value = f"{uid}"
        size = int(_)
        unpacked_values += [value] * size

    return unpacked_values


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
    result = "I am result"
    return result


if __name__ == "__main__":
    RESULT = main()
    print(f"Result: {RESULT}")
