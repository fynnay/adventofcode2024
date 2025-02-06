from dataclasses import dataclass
from pathlib import Path

from aoc import (
    PuzzleName,
    Dir,
)


@dataclass
class ClawMachine:
    a: tuple[int, int]
    b: tuple[int, int]
    prize: tuple[int, int]


def get_input_values(file_path: Path) -> list[ClawMachine]:
    values = []

    with open(file_path, 'r') as file:
        for line in file.readlines():
            if not line:
                continue

    return values


def calc_y(n: int, a: int, x: int, b: int):
    return (n - (a * x)) / b


def find_lowest_divisor(n: int, a: int, b: int, limit: int = 100) -> tuple[int, int]:
    """
    Iteratively (up to `limit`) determines the lowest factors at which a combination of `a` and `b` fit into `n`.

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
    x: int
    y: int

    for _ in range(limit):
        x = _
        i = calc_y(n, a, x, b)
        if i.is_integer():
            y = int(i)
            break
        elif i < 0:
            raise ValueError(f"Combination not possible")
    else:
        raise ValueError(f"Limit exceeded")

    return x, y


def calc_claw_machine_moves(claw_machine: ClawMachine) -> list[tuple[int, int]]:
    # Find the largest position
    xy_srcs = [claw_machine.a, claw_machine.b]
    x_sum = sum([_[0] for _ in xy_srcs])
    y_sum = sum([_[1] for _ in xy_srcs])
    xy_sum = [x_sum, y_sum]
    index_max = xy_sum.index(max(x_sum, y_sum))
    index_inv = len(xy_sum) - 1 - index_max
    indexes = [index_max, index_inv]

    values = []

    for _ in range(2):
        index = indexes[_]
        prize = claw_machine.prize[index]
        src_a = claw_machine.a[index]
        src_b = claw_machine.b[index]
        ab_min = min(src_a, src_b)
        ab_max = max(src_a, src_b)
        ab_lst = [ab_min, ab_max]
        a_index = ab_lst.index(src_a)
        b_index = ab_lst.index(src_b)
        divisor = find_lowest_divisor(
            prize,
            ab_min,
            ab_max,
        )
        x = divisor[a_index]
        y = divisor[b_index]
        values.append((x, y))

    return values


def process(input_values: list[ClawMachine]) -> tuple[int, int]:
    for _ in input_values:
        winning_moves = calc_claw_machine_moves(_)


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
