import math
import sys
from importlib import util

import pytest
import aoc


@pytest.fixture
def guard() -> tuple[tuple[int, int], tuple[int, int]]:
    """
    Returns guard's position and direction

    Returns:
        (pos, dir)
        ((x, y), (x, y))
    """
    return ((1, 1), (1, 1))


def test_rotate(guard):
    pos, direction = guard
    rotated = math.sin(direction)



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
