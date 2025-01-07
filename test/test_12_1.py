import sys
from enum import Enum
from importlib import util

import pytest
import aoc
import aoc_12_1
from aoc_12_1 import Region, Point, Land


class TestCase(Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    G = "G"
    H = "H"
    I = "I"
    J = "J"
    K = "K"


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
            self.cost = 140
        elif case_type is TestCase.B:
            self.lines = [
                "OOOOO",
                "OXOXO",
                "OOOOO",
                "OXOXO",
                "OOOOO",
            ]
            self.regions = [
                Region(
                    plant="0",
                    points=[
                        Point(0, 0), Point(1, 0), Point(2, 0), Point(3, 0), Point(4, 0),
                        Point(0, 1),              Point(2, 1),              Point(4, 1),
                        Point(0, 2), Point(1, 2), Point(2, 2), Point(3, 2), Point(4, 2),
                        Point(0, 3),              Point(2, 3),              Point(4, 3),
                        Point(0, 4), Point(1, 4), Point(2, 4), Point(3, 4), Point(4, 4),
                    ],
                    perimeter=36,
                ),
                Region(
                    plant="X",
                    points=[Point(1,1)],
                    perimeter=4,
                ),
                Region(
                    plant="X",
                    points=[Point(3, 1)],
                    perimeter=4,
                ),
                Region(
                    plant="X",
                    points=[Point(1, 3)],
                    perimeter=4,
                ),
                Region(
                    plant="X",
                    points=[Point(3, 3)],
                    perimeter=4,
                ),
            ]
            self.cost = 772
        elif case_type == TestCase.C:
            self.lines = [
                "RRRRIICCFF",
                "RRRRIICCCF",
                "VVRRRCCFFF",
                "VVRCCCJFFF",
                "VVVVCJJCFE",
                "VVIVCCJJEE",
                "VVIIICJJEE",
                "MIIIIIJJEE",
                "MIIISIJEEE",
                "MMMISSJEEE",
            ]
            self.cost = 1930
        elif case_type == TestCase.D:
            self.lines = [
                "XO",
                "OX",
            ]
            self.regions = [
                Region(
                    plant="X",
                    points=[Point(0, 0)],
                    perimeter=4,
                ),
                Region(
                    plant="O",
                    points=[Point(1, 0)],
                    perimeter=4,
                ),
                Region(
                    plant="O",
                    points=[Point(0, 1)],
                    perimeter=4,
                ),
                Region(
                    plant="X",
                    points=[Point(1, 1)],
                    perimeter=4,
                ),
            ]
            self.cost = 16
        elif case_type == TestCase.E:
            self.lines = [
                "XXOXOXX",
                "XOOOOOX",
                "OOXOXOO",
                "XOOXOOX",
                "OOXOXOO",
                "XOOOOOX",
                "XXOXOXX",
            ]
            self.cost = 1700
        elif case_type == TestCase.F:
            self.lines = [
                "----",
                "-OOO",
                "-O-O",
                "OO-O",
                "-OOO",
            ]
            self.cost = 342
        elif case_type == TestCase.G:
            self.lines = [
                "----",
                "OOO-",
                "O-O-",
                "O-OO",
                "OOO-",
            ]
            self.cost = 342
        elif case_type == TestCase.H:
            self.lines = [
                "AXAA",
                "XAAA",
                "XAAA",
                "XAAA",
            ]
            self.cost = 186
        elif case_type == TestCase.I:
            self.lines = [
                "AAAA",
                "ABCA",
                "ABCA",
                "AAAD",
            ]
            self.cost = 292
        elif case_type == TestCase.J:
            self.lines = [
                "AAAA",
                "ABCA",
                "ABCA",
                "AAAA",
            ]
            self.cost = 312
        elif case_type == TestCase.K:
            self.lines = [
                "XOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOX",
                "OXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXO",
                "XXXXXXXXXXXXXXXMXXXMXEEEEEXRRRRXXRRRRXXYXXXYXXXXXXXXXXXXXXX",
                "OXXXXXXXXXXXXXXMMXMMXEXXXXXRXXXRXRXXXRXYXXXYXXXXXXXXXXXXXXO",
                "XXXXXXXXXXXXXXXMXMXMXEEEEEXRRRRXXRRRRXXXYXYXXXXXXXXXXXXXXXX",
                "OXXXXXXXXXXXXXXMXXXMXEXXXXXRXXXRXRXXXRXXXYXXXXXXXXXXXXXXXXO",
                "XXXXXXXXXXXXXXXMXXXMXEEEEEXRXXXRXRXXXRXXXYXXXXXXXXXXXXXXXXX",
                "OXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXO",
                "XXXXCCCXXHXXXHXRRRRXXIIIIIXXSSSSXTTTTTXMXXXMXXAAAXXXSSSSXXX",
                "OXXCXXXCXHXXXHXRXXXRXXXIXXXSXXXXXXXTXXXMMXMMXAXXXAXSXXXXXXO",
                "XXXCXXXXXHHHHHXRRRRXXXXIXXXXSSSXXXXTXXXMXMXMXAAAAAXXSSSXXXX",
                "OXXCXXXCXHXXXHXRXXXRXXXIXXXXXXXSXXXTXXXMXXXMXAXXXAXXXXXSXXO",
                "XXXXCCCXXHXXXHXRXXXRXIIIIIXSSSSXXXXTXXXMXXXMXAXXXAXSSSSXXXX",
                "OXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXO",
                "XOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOX",
            ]
            self.cost = 426452
        self.perimeter = sum([_.perimeter for _ in self.regions])
        self.land = Land.from_lines(self.lines)


@pytest.fixture(params=TestCase)
def values(request):
    return Values(request.param)


def test_region_points(values):
    land = Land.from_lines(values.lines)
    points = [set(_.points) for _ in land.find_regions()]
    assert [set(_.points) for _ in values.regions] == points


def test_perimeter(values):
    land = Land.from_lines(values.lines)
    perimeter = 0
    for _ in land.find_regions():
        _.calculate_perimeter()
        perimeter += _.perimeter
    assert perimeter == values.perimeter


def test_cost(values):
    land = Land.from_lines(values.lines)
    cost = 0
    for _ in land.find_regions():
        _.calculate_perimeter()
        cost += _.cost
    assert cost == values.cost

def test_process(values):
    result = aoc_12_1.process(values.lines)
    assert result == values.cost


# @pytest.mark.skip
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
    assert result == 1450816
