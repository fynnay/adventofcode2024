import sys
from importlib import util

import pytest

import aoc
from aoc_05_1 import PuzzleInput


@pytest.fixture
def puzzle_input() -> PuzzleInput:
    puzzle_input = PuzzleInput(
        rules=[
            [2, 1, 8],
            [10, 0, 4],
        ],
        updates=[
            [5, 3, 4],
            [2, 3, 1],
            [10, 12, 59, 0, 17],
        ]
    )
    return puzzle_input


@pytest.mark.parametrize(
    ["rule", "update", "expectation"],
    [
        [
            [2, 1],
            [1, 2, 3],
            False,
        ],
        [
            [2, 1],
            [2, 3, 1],
            True,
        ],
    ]
)
def test_is_update_ordered(rule: list[int], update: list[int], expectation: bool):
    puzzle_input = PuzzleInput(
        rules=[rule],
        updates=[update],
    )
    assert puzzle_input.is_update_ordered(update) == expectation


def test_main():
    puzzle_name = aoc.PuzzleName(
        day=5,
        part=1,
    )
    puzzle_name_text = puzzle_name.build()
    input_file = aoc.Dir.build_file_path(
        aoc.directory.Dir.INPUT,
        puzzle_name,
    )
    python_file = aoc.directory.Dir.build_file_path(
        aoc.Dir.SCRIPT,
        puzzle_name,
    )
    spec = util.spec_from_file_location(puzzle_name_text, python_file)
    module = util.module_from_spec(spec)
    sys.modules[puzzle_name_text] = module  # Optional: add the module to sys.modules
    spec.loader.exec_module(module)

    result = module.main(input_file)
    assert result
