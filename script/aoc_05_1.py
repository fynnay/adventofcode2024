from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List

from aoc import PuzzleName, Dir


class InputType(Enum):
    PAGE_ORDERING_RULES = "page orgering rules"
    UPDATES = "updates"


@dataclass
class PuzzleInput:
    rules: List[List[int]]
    updates: List[List[int]]

    def __post_init__(self):
        self.rules = [[int(a), int(b)] for a, b in self.rules]
        self.updates = [[int(a) for a in _] for _ in self.updates]


def get_puzzle_input(file_path: Path) -> PuzzleInput:
    inputs = {
        InputType.PAGE_ORDERING_RULES: [],
        InputType.UPDATES: []
    }

    with open(file_path, 'r') as fil:
        lines = fil.read()

        # Beginning of file contains the rules
        target = InputType.PAGE_ORDERING_RULES
        for _ in lines:
            # After an empty line, the updates section starts
            if _ == "\n":
                target = InputType.UPDATES

            line_sanitized = _.strip("\n").strip(" ")
            if target is InputType.PAGE_ORDERING_RULES:
                values = line_sanitized.split("|")
            elif target is InputType.UPDATES:
                values = line_sanitized.split(",")

            values_sanitized = [_ for _ in values if _]
            if not values_sanitized:
                continue
            inputs[target].append(values_sanitized)

    puzzle_input = PuzzleInput(
        rules=inputs[InputType.PAGE_ORDERING_RULES],
        updates=inputs[InputType.UPDATES],
    )

    return puzzle_input


def is_updated_ordered(rules: List[List[str]], update: List[str]) -> bool:
    """
    Returns True if the `update` is ordered according to the rules, otherwise False.
    Each rule contains exactly 2 numbers.
    Rules, whose numbers don't all occur in the update are skipped.
    All applicable rules' numbers must appear in the same order in the update to be valid.
    """

    for rule in rules:
        indexes: List[int] = []

        for entry in rule:
            if entry not in update:
                # 1[...
                break
            # Apply this rule if
            # Pass: If the entry occurs in the same order as in the rule
            # Fail: If numbers are in incorrect order
            rule_index = update.index(entry)
            indexes.append(rule_index)
        else:
            # Fail: If index do not appear in sequential order
            indexes_sorted = sorted(indexes)
            if not indexes_sorted == indexes:
                # break 2[ ...
                break

        # ...]1 to skip this rule if an entry does not occur in the update
        continue
    else:
        # All rules passed
        return True

    # ...]2 Failed a rule
    return False


def process(puzzle_input: PuzzleInput) -> int:
    """
    Returns the sum of all correctly ordered updates' middle entry
    """
    middle_entries = []

    for update in puzzle_input.updates:
        is_ordered = is_updated_ordered(puzzle_input.rules, update)
        if not is_ordered:
            continue

        middle_index = len(update) // 2
        middle_entry = update[middle_index]
        middle_entries.append(middle_entry)

    numbers = [int(_) for _ in middle_entries]
    return sum(numbers)


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
    return result


if __name__ == "__main__":
    main()
