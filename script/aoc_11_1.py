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
            values.extend([int(_) for _ in line.split(" ")])

    return values


def process(input_values: list[int], iterations: int = 25):
    values = input_values

    for _ in range(iterations):
        indexes = len(values) - 1
        index: int = 0
        print(f"Running iteration #{_:02d}")
        while True:
            if index > indexes:
                break
            value = values[index]
            # print(f"{index}: {value}")
            text = str(value)
            count = len(text)
            half = count // 2
            values.pop(index)
            increment = 1
            if count % 2 == 0:
                left = int(text[:half])
                right = int(text[half:])
                values.insert(index, right)
                values.insert(index, left)
                increment = 2
            elif value == 0:
                values.insert(index, 1)
            else:
                values.insert(index, value * 2024)

            indexes = len(values) - 1
            index += increment

    # print(values)

    return len(values)


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
