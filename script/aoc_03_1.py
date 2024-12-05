import re
from pathlib import Path
from typing import List
from aoc import PuzzleName, Dir


def get_valid_sections(text: str) -> List[re.Match]:
    pattern = re.compile(r"mul\((?P<x>\d{1,3}),(?P<y>\d{1,3})\)")
    sections = []

    for _ in pattern.finditer(text):
        sections.append(_)

    return sections


def process_sections(sections: List[re.Match]):
    results = []

    for _ in sections:
        x = int(_.group("x"))
        y = int(_.group("y"))
        results.append(x * y)

    return results


def main(file_path: Path = None):
    script_path = Path(__file__)
    puzzle_name = PuzzleName.parse(script_path.stem)
    file_path = file_path or Dir.build_file_path(
        Dir.INPUT,
        puzzle_name=PuzzleName(
            day=puzzle_name.day,
            part=puzzle_name.part,
        )
    )

    with open(file_path, 'r') as fil:
        content = fil.read()

    sections_valid = get_valid_sections(content)
    sections_processed = process_sections(sections_valid)
    result = sum(sections_processed)
    return result


if __name__ == "__main__":
    print("Result: ", main())

