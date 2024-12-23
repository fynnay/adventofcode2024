import sys
from importlib import util

import pytest

import aoc
from aoc_09_1 import unpack, reorder


@pytest.fixture
def input_values():
    return list("12345")


@pytest.fixture
def unpacked_values():
    return list("0..111....22222")


@pytest.fixture
def reordered_values():
    return [
        list("0..111....22222"),
        list("02.111....2222."),
        list("022111....222.."),
        list("0221112...22..."),
        list("02211122..2...."),
        list("022111222......"),
    ]


def test_unpack(input_values: list[str],
                unpacked_values
                ):
    result = unpack(input_values)
    assert result == unpacked_values


def test_reorder(
        unpacked_values: list[str],
        reordered_values: list[str],
        ):
    result = reorder(unpacked_values)
    assert result == reordered_values


def test_checksum(
        reordered_values
        ):
    pass


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
