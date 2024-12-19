import sys
from importlib import util

import pytest

import aoc
from aoc_08_1 import (
    MATRIX,
    NODE,
    get_antennas,
    group_aligned_nodes,
    place_anti_nodes,
    RECTANGLE,
    filter_far_nodes,
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
def test_get_antennas(_matrix, expected: list[NODE]):
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
            {
                frozenset({((0, 0), 'a'), ((3, 3), 'a')}),
                frozenset({((2, 3), 'b'), ((1, 1), 'b')})
            }
            ,
        ],
        [
            [
                "......#....#",
                "...#....0...",
                "....#0....#.",
                "..#....0....",
                "....0....#..",
                ".#....A.....",
                "...#........",
                "#......#....",
                "........A...",
                ".........A..",
                "..........#.",
                "..........#.",
            ],
            {
                frozenset([((8, 1), "0"), ((5, 2), "0")]),
                frozenset([((8, 1), "0"), ((7, 3), "0")]),
                frozenset([((8, 1), "0"), ((4, 4), "0")]),
                frozenset([((5, 2), "0"), ((7, 3), "0")]),
                frozenset([((5, 2), "0"), ((4, 4), "0")]),
                frozenset([((7, 3), "0"), ((4, 4), "0")]),
                frozenset([((6, 5), "A"), ((8, 8), "A")]),
                frozenset([((6, 5), "A"), ((9, 9), "A")]),
                frozenset([((8, 8), "A"), ((9, 9), "A")]),
            }
        ]
    ]
)
def test_group_aligned_nodes(_matrix, expected: set[frozenset[NODE]]):
    antennas = get_antennas(_matrix)
    antennas_aligned = group_aligned_nodes(antennas)
    assert antennas_aligned == expected


@pytest.mark.parametrize(
    ["node_groups", "expected"],
    [
        [
            {
                frozenset([((8, 1), "0"), ((5, 2), "0")]),
                frozenset([((8, 1), "0"), ((7, 3), "0")]),
                frozenset([((8, 1), "0"), ((4, 4), "0")]),
                frozenset([((5, 2), "0"), ((7, 3), "0")]),
                frozenset([((5, 2), "0"), ((4, 4), "0")]),
                frozenset([((7, 3), "0"), ((4, 4), "0")]),
                frozenset([((6, 5), "A"), ((8, 8), "A")]),
                frozenset([((6, 5), "A"), ((9, 9), "A")]),
                frozenset([((8, 8), "A"), ((9, 9), "A")]),
            },
            {
                ((6, 0), "#"),
                ((11, 0), "#"),
                ((3, 1), "#"),
                ((4, 2), "#"),
                ((10, 2), "#"),
                ((2, 3), "#"),
                ((9, 4), "#"),
                ((1, 5), "#"),
                ((6, 5), "#"),
                ((3, 6), "#"),
                ((0, 7), "#"),
                ((7, 7), "#"),
                ((10, 10), "#"),
                ((10, 11), "#"),
                # outside matrix
                ((9, -1), "#"),
                ((12, -2), "#"),
                ((12, 13), "#"),
            }
        ]
    ]
)
def test_place_anti_nodes(node_groups: set[frozenset[NODE]], expected: set[NODE]):
    anti_nodes = place_anti_nodes(node_groups)
    _matches = expected.intersection(anti_nodes)
    _missing = expected.difference(anti_nodes)
    _overflow = anti_nodes.difference(expected)
    assert anti_nodes == expected

@pytest.mark.parametrize(
    ["nodes", "bounds", "expected"],
    [
        [
            [
                ((10, 10), "#"),
                ((10, 11), "#"),
                # outside matrix
                ((9, -1), "#"),
                ((12, -2), "#"),
                ((12, 13), "#"),
            ],
            (
                    (0, 0),
                    (11, 11)
            ),
            [
                ((10, 10), "#"),
                ((10, 11), "#"),
            ],
        ]
    ]
)
def test_filter_far_nodes(nodes: list[NODE], bounds: RECTANGLE, expected: list[NODE]):
    result = filter_far_nodes(nodes, bounds)
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
    assert result == 329
