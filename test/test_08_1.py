import sys
from importlib import util

import pytest

import aoc
from aoc_08_1 import MATRIX, POINT, VECTOR, get_cross_section


@pytest.fixture
def matrix_1() -> MATRIX:
    text = [
        "123456",
        "123456",
        "123456",
    ]

    lines = [[i for i in _] for _ in text]

    return lines


@pytest.mark.parametrize(
    ["point", "vector", "length", "expected"],
    [
        [(0, 0), (1, 1), None, ["1", "2", "3"]],
        [(0, 0), (0, 1), None, ["1", "1", "1"]],
        [(0, 0), (1, 0), None, ["1", "2", "3", "4", "5", "6"]],
        [(0, 0), (2, 1), None, ["1", "3", "5"]],
        [(0, 0), (2, 2), None, ["1", "3"]],
        [(0, 0), (1, 1), 2, ["1", "2"]],
        [(0, 0), (0, 1), 2, ["1", "1"]],
        [(0, 0), (1, 0), 1, ["1"]],
        [(0, 0), (2, 1), 0, []],
    ],
)
def test_get_cross_section(matrix_1: MATRIX, point: POINT, vector: VECTOR, length: int, expected: list[str]):
    result = get_cross_section(
        matrix_1,
        point,
        vector,
        length,
    )
    assert result == expected


def test_main():
    puzzle_name = aoc.PuzzleName(
        day=8,
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
