import sys
from importlib import util

import pytest
import aoc
import aoc_06_1


@pytest.fixture
def guard() -> tuple[tuple[int, int], tuple[int, int]]:
    """
    Returns guard's position and direction

    Returns:
        (pos, dir)
        ((x, y), (x, y))
    """
    return (1, 1), (1, 0)


@pytest.mark.parametrize(
    ["vector", "direction", "expected"],
    [
        # counterclockwise
        [(1, 0), 0, (0, 1)],
        [(0, 1), 0, (-1, 0)],
        [(-1, 0), 0, (0, -1)],
        [(0, -1), 0, (1, 0)],
        # clockwise
        [(1, 0), 1, (0, -1)],
        [(0, -1), 1, (-1, 0)],
        [(-1, 0), 1, (0, 1)],
        [(0, 1), 1, (1, 0)],
    ]
)
def test_rotate(vector: tuple[int, int], direction: int, expected: tuple[int, int]):
    """
    Rotate the incoming vector to the right by 90 degrees
    """
    rotated = aoc_06_1.rotate(vector, direction)
    assert rotated == expected


@pytest.mark.parametrize(
    ["symbol", "expected"],
    [
        ["^", (-0, +1)],
        ["v", (-0, -1)],
        ["<", (-1, -0)],
        [">", (+1, -0)],
    ],
)
def test_get_guard_vector(symbol: str, expected: tuple[int, int]):
    assert aoc_06_1.get_vector(symbol) == expected


def test_guard_route():
    puzzle_input = [
        ["#", ".", ".", "."],
        [".", ".", ".", "#"],
        ["^", ".", ".", "."],
        ["#", ".", ".", "."],
        [".", ".", "#", "."],
    ]
    guard_route = aoc_06_1.process(puzzle_input)
    print(guard_route)


def test_main():
    puzzle_name = aoc.PuzzleName(
        day=6,
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
    assert result == 4964
