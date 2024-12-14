import sys
from importlib import util

import pytest
import aoc
import aoc_07_1


@pytest.fixture
def something():
    return


@pytest.mark.parametrize(
    ["positions", "operators", "expected"],
    [
        [1, ["*", "+"],
         [
             ("*", ),
             ("+", ),
         ]],
        [2, ["*", "+"],
         [
             ("*", "*"),
             ("*", "+"),
             ("+", "*"),
             ("+", "+"),
         ]],
    ]
)
def test_combinations(positions: int, operators: list[str], expected: list[list[str]]):
    combinations = aoc_07_1.get_combinations(positions, operators)
    for _ in combinations:
        print(_)
    assert combinations == expected

def test_main():
    puzzle_name = aoc.PuzzleName(
        day=7,
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
    assert result == 2500
