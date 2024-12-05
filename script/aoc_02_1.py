from pathlib import Path
from typing import List, Tuple

from aoc import (
    PuzzleName,
    Dir,
)


def get_input_values(file_path: Path) -> List[List[int]]:
    values = []

    with open(file_path, 'r') as file:
        for line in file.readlines():
            if not line:
                continue
            vals = [int(_) for _ in line.split(" ")]
            values.append(vals)

    return values


def is_report_safe(report: List[int]) -> bool:
    initial_vector = None

    for index, level in enumerate(report):
        # If reached last level, it's safe
        if index >= len(report) - 1:
            return True

        # Compare against next level
        next_level = report[index + 1]
        diff = level - next_level
        dist = abs(diff)
        vect = +1 if diff > 0 else -1

        # Unsafe if distance between levels less than 1 or more than 3
        if not 1 <= dist <= 3:
            return False

        # In first test, remember first vector (1=up, -1=down)
        # If subsequent tests have different vector they're unsafe
        if initial_vector is None:
            initial_vector = vect
            continue
        else:
            if vect != initial_vector:
                return False


def process_reports(reports: List[List[int]]) -> Tuple[List[int], List[int], List[int]]:
    safe_reports = []
    unsafe_reports = []
    failed_reports = []

    for report in reports:
        result = is_report_safe(report)
        if result is True:
            safe_reports.append(result)
        elif result is False:
            unsafe_reports.append(result)
        else:
            failed_reports.append(result)

    return safe_reports, unsafe_reports, failed_reports


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
    reports = get_input_values(file_path)
    safe_reports, unsafe_reports, failed_reports = process_reports(reports)
    return len(safe_reports)


if __name__ == "__main__":
    RESULT = main()
    print(f"Result: {RESULT}")
