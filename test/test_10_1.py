import sys
from importlib import util
from enum import Enum

import pytest
import aoc
import aoc_10_1



class TestCase(Enum):
    A = "A"
    B = "B"
    C = "C"


class Values:
    def __init__(self, case_type: TestCase):
        self.case_type = case_type
        self.input: aoc_10_1.MAP = []
        self.trail_score: int = None

        if case_type is TestCase.A:
            self.input = "0123\n1234\n8765\n9876\n"
            self.map: aoc_10_1.MAP = [
                [0,1,2,3],
                [1,2,3,4],
                [8,7,6,5],
                [9,8,7,6],
            ]
            self.tails = [
                [
                    (0,0),
                    (1,0),
                    (2,0),
                    (3,0),
                    (3,1),
                    (3,2),
                    (3,3),
                    (2,3),
                    (1,3),
                    (0,3),
                ]
            ]
            self.trail_scores = [
                1,
            ]


@pytest.fixture(params=TestCase)
def values(request):
    return Values(request.param)


def test_main():
    puzzle_name = aoc.PuzzleName(
        day=10,
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
