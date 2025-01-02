import sys
from enum import Enum
from importlib import util

import pytest
import aoc


class Case(Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"


class Values:
    def __init__(self, case: Case):
        self.value_1 = None
        self.value_2 = None

        if case is Case.A:
            self.value_1 = 1
            self.value_2 = 2


@pytest.fixture(params=Case)
def values(request):
    return Values(request.param)


def test_something(values):
    assert values.value_1 == values.value_2


def test_main():
    puzzle_name = aoc.PuzzleName(
        day=0,
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
