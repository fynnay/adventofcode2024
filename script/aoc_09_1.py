import re
from pathlib import Path

from aoc import (
    PuzzleName,
    Dir,
)
import logging

logging.basicConfig(format="%(asctime)s [%(levelname)s] %(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)


def get_input_values(file_path: Path) -> list[str]:
    values = []

    with open(file_path, 'r') as file:
        for line in file.readlines():
            if not line:
                continue
            values += [_ for _ in line if _]

    return values


def unpack(input_values: list[str]) -> list[str]:
    logger.info("unpacking...")
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


def reorder(unpacked_values: list[str]) -> list[list[str]]:
    logger.info("reordering...")

    num_indexes: int = len(unpacked_values) - 1
    data_index: int = num_indexes
    data_sorted: list[str] = []

    for index, value in enumerate(unpacked_values):
        logger.debug(f"{index}/{num_indexes}: {value}")

        # Cancel if we have crossed the current index
        if data_index < index:
            break

        # Existing data stays where it is
        if value != ".":
            data_sorted.append(value)
            continue

        # Pick data from end of file to fill free space
        for _ in range(data_index, 0, -1):
            data_value = unpacked_values[_]
            if data_value != ".":
                data_index = _
                break

        # Cancel if we have crossed the current index while searching for data
        if data_index < index:
            break

        data_sorted.append(data_value)
        data_index -= 1

    free_space_amount = len(unpacked_values) - len(data_sorted)
    free_space = ["."] * free_space_amount
    reordered_values = data_sorted + free_space
    return reordered_values


def calculate_checksum(reordered_values: list[str]) -> int:
    logger.info("calculating...")
    total = 0

    for index, uid in enumerate(reordered_values):
        if not uid.isnumeric():
            break
        r = index * int(uid)
        total += r

    return total


def process(input_values: list[str]):
    logger.info("Processing...")
    unpacked_values = unpack(input_values)
    reordered_values = reorder(unpacked_values)[-1]
    checksum = calculate_checksum(reordered_values)
    return checksum


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
