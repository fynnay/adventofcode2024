import sys
from enum import Enum
from importlib import util

import pytest

import aoc
from aoc_09_1 import unpack, reorder, calculate_checksum


class ValueType(Enum):
    SHORT = "short"
    LONG = "long"


class Value:
    def __init__(
            self,
            value_type: ValueType,
    ):
        self.value_type = value_type
        self.input: list[str]
        self.unpacked: list[str]
        self.reordered: list[list[str]]
        self.checksum: int

        if value_type == ValueType.SHORT:
            self.input = list("12345")
            self.unpacked = list("0..111....22222")
            self.reordered = [
                list("0..111....22222"),
                list("02.111....2222."),
                list("022111....222.."),
                list("0221112...22..."),
                list("02211122..2...."),
                list("022111222......"),
            ]
            self.checksum = 7
        elif value_type == ValueType.LONG:
            self.input = list("011111111111111111111111")
            self.unpacked = [
                "0", ".", "1", ".", "2", ".", "3", ".", "4", ".", "5", ".", "6", ".", "7", ".", "8", ".", "9", ".", "10", ".", "11", "."
            ]
            self.reordered = [
                ["0", ".", "1", ".", "2", ".", "3", ".", "4", ".", "5", ".", "6", ".", "7", ".", "8", ".", "9", ".", "10", ".", "11", "."],
                ["0", "11", "1", ".", "2", ".", "3", ".", "4", ".", "5", ".", "6", ".", "7", ".", "8", ".", "9", ".", "10", ".", ".", "."],
                ["0", "11", "1", "10", "2", ".", "3", ".", "4", ".", "5", ".", "6", ".", "7", ".", "8", ".", "9", ".", ".", ".", ".", "."],
                ["0", "11", "1", "10", "2", "9", "3", ".", "4", ".", "5", ".", "6", ".", "7", ".", "8", ".", ".", ".", ".", ".", ".", "."],
                ["0", "11", "1", "10", "2", "9", "3", "8", "4", ".", "5", ".", "6", ".", "7", ".", ".", ".", ".", ".", ".", ".", ".", "."],
                ["0", "11", "1", "10", "2", "9", "3", "8", "4", "7", "5", ".", "6", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
                ["0", "11", "1", "10", "2", "9", "3", "8", "4", "7", "5", "6", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            ]
            self.checksum = 0+10+18+24+28+30


@pytest.fixture(scope="module", params=ValueType)
def value(request) -> Value:
    value = Value(request.param)
    yield value


def test_unpack(value):
    result = unpack(value.input)
    assert result == value.unpacked


def test_reorder(value: Value):
    result = reorder(value.unpacked)
    assert result == value.reordered


def test_checksum(value: Value):
    assert calculate_checksum(value.reordered[-1]) == value.checksum


def test_main():
    puzzle_name = aoc.PuzzleName(
        day=9,
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
