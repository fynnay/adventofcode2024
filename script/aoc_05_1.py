from enum import Enum
from pathlib import Path
from typing import Tuple, List, Dict

from aoc import PuzzleName, Dir


class InputType(Enum):
    PAGE_ORDERING_RULES = "page orgering rules"
    UPDATES = "updates"


def get_puzzle_input(file_path: Path) -> Dict[InputType, List[List[str]]]:
    inputs = {
        InputType.PAGE_ORDERING_RULES: [],
        InputType.UPDATES: []
    }
    with open(file_path, 'r') as fil:
        lines = fil.readlines()
        target = InputType.PAGE_ORDERING_RULES
        for _ in lines:
            if _ == "\n":
                target = InputType.UPDATES
            if target is InputType.PAGE_ORDERING_RULES:
                value = _.strip("\n").split("|")
            elif target is InputType.UPDATES:
                value = _.strip("\n").split(",")

            inputs[target].append(value)

    return inputs


def is_updated_ordered(rules: List[List[str]], update: List[str]) -> bool:

    for rule in rules:
        index_1 = 0
        index_2 = 0

        for entry in rule:
            if entry not in update:
                break
            # Apply this rule if
            # Pass: If numbers occur in the correct order
            # Fail: If numbers are in incorrect order
            index_1 = update.index(entry)
            index_2 = update.index(entry)
        else:
            continue

        if index_1 < index_2:
            pass

        # Skip this rule if an entry does not occur in the update
        continue
    else:
        # All rules passed
        return True

    # Failed a rule
    return False


def process(puzzle_input: Dict[InputType, List[List[str]]]):
    rules = puzzle_input[InputType.PAGE_ORDERING_RULES]
    updates = puzzle_input[InputType.UPDATES]

    for update in updates:
        is_ordered = False



def main(
        file_path: Path = None
):
    script_path = Path(__file__)
    puzzle_name = PuzzleName.parse(script_path.stem)
    file_path = file_path or Dir.build_file_path(
        Dir.INPUT,
        puzzle_name=PuzzleName(
            day=puzzle_name.day,
            part=puzzle_name.part,
        )
    )

    puzzle_input = get_puzzle_input(file_path)
    result = process(puzzle_input)
    return


if __name__ == "__main__":
    main()
