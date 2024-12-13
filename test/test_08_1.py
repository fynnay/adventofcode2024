import sys
from importlib import util

import pytest

import aoc
from aoc_08_1 import (
    MATRIX,
    POINT,
    VECTOR,
    get_line,
    LINE,
    find_resonant_circuits,
    ELEMENT,
    get_antennas,
)


@pytest.fixture
def matrix_1() -> MATRIX:
    text = [
        "123456",
        "123456",
        "123456",
    ]

    lines = [[i for i in _] for _ in text]

    return lines


@pytest.fixture
def matrix_2() -> MATRIX:
    text = [
        "..........",
        "..........",
        "..........",
        "....a.....",  # 4,3
        "........a.",  # 8,4
        ".....a....",  # 5,5
        "..........",
        "..........",
        "..........",
        "..........",
    ]

    lines = [[i for i in _] for _ in text]

    return lines


@pytest.fixture
def matrix_3() -> MATRIX:
    text = [
        "..........",
        "...#......",
        "#.........",
        "....a.....",
        "........a.",
        ".....a....",
        "..#.......",
        "......#...",
        "..........",
        "..........",
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
        [(5, 2), (1, 1), None, ["6"]],
        [(5, 2), (-1, -1), None, ["6", "5", "4"]],
        [(5, 2), (-2, -1), None, ["6", "4", "2"]],
        [(5, 2), (-2, -2), None, ["6", "4"]],
    ],
)
def test_get_cross_section(matrix_1: MATRIX, point: POINT, vector: VECTOR, length: int, expected: list[str]):
    result = get_line(
        matrix_1,
        point,
        vector,
        length,
    )
    assert result == expected


@pytest.mark.parametrize(
    ["point", "vector", "expected"],
    [
        [
            (4, 3),
            (1, 2),
            [
                ["a", "a", ".", "."],
            ],
        ]
    ]
)
def test_get_resonant_circuits(matrix_2: MATRIX, point: POINT, vector: VECTOR, expected: list[LINE]):
    # Get circuits from matrix
    # TODO: Do separate check
    circuits = [
        get_line(
            matrix_2,
            point,
            vector,
            None
        )
    ]

    # Get resonant circuits and flatten nodes to check result
    resonant_circuits = find_resonant_circuits(circuits)
    nodes = [[a[1] for a in b] for b in resonant_circuits]

    assert nodes == expected


@pytest.mark.parametrize(
    ["_matrix", "expected"],
    [
        [
            [
                list("....b"),
                list(".a.b."),
                list("....."),
                list("...a."),
            ],
            [
                ((4,0), "b"),
                ((1,1), "a"), ((3,1), "b"),
                ((3,3), "a"),
            ]
        ]
    ]
)
def test_get_antennas(_matrix, expected: list[ELEMENT]):
    antennas = get_antennas(
        _matrix
    )
    assert antennas == expected


@pytest.mark.parametrize(
    ["_matrix", "expected"],
    [
        [
            [
                "a...",
                ".b..",
                "....",
                "..ba",
            ],
            [
                [((1,1), "b"), ((2,3), "b")]
            ]
        ]
    ]
)
def test_get_resonating_antennas(_matrix, expected: list[ELEMENT]):
    result = get_resonating_antennas()
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
