from pathlib import Path

from aoc import (
    PuzzleName,
    Dir,
)


POINT = tuple[int, int]
VECTOR = tuple[int, int]
ELEVATION = int
MAP = list[list[ELEVATION]]
NODE = tuple[POINT, ELEVATION]


class Direction(Enum):
    UP: VECTOR = (0, 1)
    DOWN: VECTOR = (0, -1)
    RIGHT: VECTOR = (1, 0)
    LEFT: VECTOR = (-1, 0)


def get_input_values(file_path: Path) -> MAP
    values = []

    with open(file_path, 'r') as file:
        for line in file.readlines():
            if not line:
                continue
            values.append([int(_) for _ in line])

    return values


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
