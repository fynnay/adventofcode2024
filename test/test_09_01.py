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
            self.input = list("01234567891")
            self.unpacked = [
                "0", ".", "2", "2", ".", ".", ".", "4", "4", "4", "4", ".", ".", ".", ".", ".", "6", "6", "6", "6",
                "6", "6", ".", ".", ".", ".", ".", ".", ".", "8", "8", "8", "8", "8", "8", "8", "8", ".", ".", ".",
                ".", ".", ".", ".", ".", ".", "11", "11", "11", "11","11", "11", "11", "11", "11", "11"
            ]
            self.reordered = [
                "0", "11", "2", "2", "11", "11", "11", "4", "4", "4", "4", "11", "11", "11", "11", "11", "6", "6", "6", "6",
                "6", "6", "11", "8", "8", "8", "8", "8", "8", "8", "8", ".", ".", ".", ".", ".", ".", ".", ".", ".",
                ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."
            ]
            self.checksum = 859


@pytest.fixture(scope="module", params=ValueType)
def input_values(request: pytest.FixtureRequest):
    values = {
        "short": list("12345"),
        "long": list("01234567891")
    }
    yield values.get(request.param)


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


@pytest.fixture
def checksum_value() -> int:
    return 7


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
        reordered_values: list[str],
        checksum_value: int,
        ):
    assert calculate_checksum(reordered_values[-1]) == checksum_value


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
