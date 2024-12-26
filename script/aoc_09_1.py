import re
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
        unpacked_values += [value] * max(size, 1)

    return unpacked_values


def reorder(unpacked_values: list[str]) -> list[list[str]]:
    reordering_steps: list[list[str]] = []
    reordered_values: list[str] = list(unpacked_values)

    num_indexes = len(unpacked_values) - 1
    for index, value in enumerate(unpacked_values):
        if value != ".":
            continue

        reordering_steps.append(list(reordered_values))

        reverse_index = len(reordered_values)
        for reverse_index, data_value in enumerate(reversed(reordered_values)):
            if data_value != ".":
                break

        data_index = num_indexes - reverse_index
        if data_index < index:
            break

        reordered_values.pop(data_index)
        reordered_values.insert(data_index, ".")
        reordered_values.pop(index)
        reordered_values.insert(index, data_value)

    return reordered_values


def calculate_checksum(reordered_values: list[str]) -> int:
    values = []

    for _ in range(0, len(reordered_values), 2):
        a = reordered_values[_]
        b = reordered_values[_ + 1]
        if not a.isnumeric() or not b.isnumeric():
            break
        r = int(a) * int(b)
        values.append(r)

    return sum(values)


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
