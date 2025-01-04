import contextlib
import sys
from enum import Enum
from importlib import util

import pytest
import aoc
import aoc_13_1
from aoc_13_1 import ClawMachine


class Case(Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"


class Values:
    def __init__(self, case: Case):
        self.a = None
        self.b = None
        self.prize = None
        self.expected = None

        if case is Case.A:
            self.a = (94, 34)
            self.b = (22, 67)
            self.prize = (8400, 5400)
            self.expected = (80, 40)
        elif case is Case.B:
            self.a = (26, 66)
            self.b = (67, 21)
            self.prize = (12748, 12176)
            self.expected = ValueError()
        elif case is Case.C:
            self.a = (17, 86)
            self.b = (84, 37)
            self.prize = (7870, 6450)
            self.expected = (38, 86)
        elif case is Case.D:
            self.a = (69, 23)
            self.b = (27, 71)
            self.prize = (18641, 10279)
            self.expected = ValueError()

        self.claw_machine = ClawMachine(
            self.a,
            self.b,
            self.prize,
        )


@pytest.fixture(params=Case)
def values(request):
    return Values(request.param)


def test_calc_claw_machine_winning_moves(values):

    def run():
        return aoc_13_1.calc_claw_machine_winning_moves(
            values.claw_machine
        )

    if isinstance(values.expected, Exception):
        context = pytest.raises(values.expected.__class__)
        with context:
            run()
    else:
        assert run() == values.expected


@pytest.mark.skip
def test_main():
    puzzle_name = aoc.PuzzleName(
        day=13,
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
