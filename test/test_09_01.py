import sys
from enum import Enum
from importlib import util

import pytest

import aoc
from aoc_09_1 import unpack, reorder, calculate_checksum


class ValueType(Enum):
    SHORT = "short"
    MEDIUM = "medium"
    LONG = "long"
    UNEVEN = "uneven"

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
            self.reordered = list("022111222......")
            self.checksum = (0*0) + (1*2) + (2*2) + (3*1) + (4*1) + (5*1) + (6*2) + (7*2) + (8*2)
        elif value_type == ValueType.MEDIUM:
            self.input = list("2333133121414131402")
            self.unpacked = list("00...111...2...333.44.5555.6666.777.888899")
            self.reordered = list("0099811188827773336446555566..............")
            self.checksum = 1928
        elif value_type == ValueType.LONG:
            self.input = list("011111111111111111111111")
            self.unpacked = list(".1.2.3.4.5.6.7.8.9.") + ["10", ".", "11", "."]
            self.reordered = ["11", "1", "10"] + list("29384756............")
            self.checksum = (0*11) + (1*1) + (2*10) + (3*2) + (4*9) + (5*3) + (6*8) + (7*4) + (8*7) + (9*5) + (10*6)
        elif value_type == ValueType.UNEVEN:
            self.input = list("113")
            self.unpacked = list("0.111")
            self.reordered = list("0111.")
            self.checksum = (0*0) + (1*1) + (2*1) + (3*1)


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
    assert calculate_checksum(value.reordered) == value.checksum


@pytest.mark.skip
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
