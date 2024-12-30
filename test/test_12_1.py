import sys
from enum import Enum
from importlib import util

import pytest
import aoc
from aoc_12_1 import Node, Region, Point, Land


class TestCase(Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"


class Values:
    def __init__(self, case_type: TestCase):
        self.case_type = case_type
        self.lines: list[list[str]] = []
        self.regions: list[Region] = []
        self.perimeter: int = 0
        self.cost: int = 0

        if case_type is TestCase.A:
            self.lines = [
                "AAAA",
                "BBCD",
                "BBCC",
                "EEEC",
            ]
            self.regions = [
                Region(
                    plant="A",
                    points=[
                        Point(0, 0),
                        Point(1, 0),
                        Point(2, 0),
                        Point(3, 0),
                    ],
                    perimeter=10,
                ),
                Region(
                    plant="B",
                    points=[
                        Point(0, 1),
                        Point(0, 2),
                        Point(1, 2),
                        Point(1, 1),
                    ],
                    perimeter=8,
                ),
                Region(
                    plant="C",
                    points=[
                        Point(2, 1),
                        Point(2, 2),
                        Point(3, 2),
                        Point(3, 3),
                    ],
                    perimeter=10,
                ),
                Region(
                    plant="D",
                    points=[
                        Point(3, 1),
                    ],
                    perimeter=4,
                ),
                Region(
                    plant="E",
                    points=[
                        Point(0, 3),
                        Point(1, 3),
                        Point(2, 3),
                    ],
                    perimeter=8,
                )
            ]
            self.perimeter = sum([_.perimeter for _ in self.regions])
            self.cost = 1
        elif case_type is TestCase.B:
            pass
        self.map = Land.from_lines(self.lines)


@pytest.fixture(params=TestCase)
def values(request):
    return Values(request.param)


def test_regions(values):
    land = Land.from_lines(values.lines)
    regions = land.find_regions()
    assert values.regions == regions


def test_perimeter(values):
    land = Land.from_lines(values.lines)
    perimeter = 0
    for _ in land.find_regions():
        _.calculate_perimeter()
        perimeter += _.perimeter
    assert perimeter == values.perimeter


def test_main():
    puzzle_name = aoc.PuzzleName(
        day=12,
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
