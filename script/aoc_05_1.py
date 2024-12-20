from dataclasses import dataclass
from pathlib import Path
from typing import List

from aoc import PuzzleName, Dir


@dataclass
class PuzzleInput:
    rules: List[List[int]]
    updates: List[List[int]]

    def is_update_ordered(
            self,
            update: list[int],
    ) -> bool:
        """
        Returns True if the `update` is ordered according to the rules, otherwise False.
        Each rule contains exactly 2 numbers.
        Rules, whose numbers don't all occur in the update are skipped.
        All applicable rules' numbers must appear in the same order in the update to be valid.
        """
        for rule in self.rules:
            indexes: list[int] = []

            for entry in rule:
                if entry not in update:
                    # 1...
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
                    # break 2...
                    break

            # ...1 to skip this rule if an entry does not occur in the update
            continue
        else:
            # All rules passed
            return True

        # ...2 Failed a rule
        return False


def get_puzzle_input(file_path: Path) -> PuzzleInput:
    # Read file content
    with open(file_path, 'r') as fil:
        lines = fil.read()

    # File contains rules first and then updates
    rules_raw, updates_raw = lines.split("\n\n")
    rules_lines = rules_raw.split("\n")
    updates_lines = updates_raw.split("\n")
    rules = []
    updates = []

    for line in rules_lines:
        line_sanitized = line.strip("\n").strip(" ")
        values = line_sanitized.split("|")
        numbers = [int(_) for _ in values if _]
        if not numbers:
            continue
        rules.append(numbers)

    for line in updates_lines:
        line_sanitized = line.strip("\n").strip(" ")
        values = line_sanitized.split(",")
        numbers = [int(_) for _ in values if _]
        if not numbers:
            continue
        updates.append(numbers)

    puzzle_input = PuzzleInput(
        rules=rules,
        updates=updates,
    )

    return puzzle_input


def process(puzzle_input: PuzzleInput) -> int:
    """
    Returns the sum of all correctly ordered updates' middle entry
    """
    middle_entries = []

    for update in puzzle_input.updates:
        is_ordered = puzzle_input.is_update_ordered(update)

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
    print(f"Result: {main()}")
