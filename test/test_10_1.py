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
    D = "D"
    E = "E"


class Values:
    def __init__(self, case_type: TestCase):
        self.case_type = case_type
        self.lines: aoc_10_1.MAP = []
        self.score: int = 0

        if case_type is TestCase.A:
            self.lines = [
                "0123",
                "1234",
                "8765",
                "9876",
            ]
            self.head_scores = [
                1,
            ]
            self.score = 1

        elif case_type is TestCase.B:
            self.lines = [
                "...0...",
                "...1...",
                "...2...",
                "6543456",
                "7.....7",
                "8.....8",
                "9.....9",
            ]
            self.head_scores = [
                2,
            ]
            self.score = 2

        elif case_type is TestCase.C:
            self.lines = [
                "..90..9",
                "...1.98",
                "...2..7",
                "6543456",
                "765.987",
                "876....",
                "987....",
            ]
            self.head_scores = [
                4,
            ]
            self.score = 4

        elif case_type is TestCase.D:
            self.lines = [
                "10..9..",
                "2...8..",
                "3...7..",
                "4567654",
                "...8..3",
                "...9..2",
                ".....01",
            ]
            self.head_scores = [
                1, 2,
            ]
            self.score = 3

        elif case_type is TestCase.E:
            self.lines = [
                "89010123",
                "78121874",
                "87430965",
                "96549874",
                "45678903",
                "32019012",
                "01329801",
                "10456732",
            ]
            self.head_scores = [
                5, 6, 5, 3, 1, 3, 5, 3, 5
            ]
            self.score = 36

        self.map = aoc_10_1.Map.from_lines(self.lines)


@pytest.fixture(params=TestCase)
def values(request):
    return Values(request.param)


def test_trail_head_scores(values):
    tmap = values.map
    heads = tmap.get_trail_heads()
    peaks: list[set[aoc_10_1.Node]] = []
    for head in heads:
        peaks.append(set(tmap.find_peaks(head)))
    head_scores = [
        len(_) for _ in peaks
    ]
    assert head_scores == values.head_scores


def test_score(values):
    tmap = values.map
    score = aoc_10_1.process(tmap)
    assert score == values.score


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
    assert result == 624
