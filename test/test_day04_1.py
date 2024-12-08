import sys
from importlib import util
from typing import List, Tuple

import pytest

import aoc
import aoc_04_1


@pytest.mark.parametrize(
    ["current", "minimum", "maximum", "expected"],
    [
        [0, 0, 5, (None, 1)],
        [1, 0, 5, (0, 2)],
        [5, 0, 5, (4, None)],
    ]
)
def test_get_next_indices(
        current: int,
        minimum: int,
        maximum: int,
        expected: int | None
        ):
    result = aoc_04_1.get_next_indices(current, minimum, maximum)
    assert result == expected


@pytest.fixture
def word() -> str:
    return "XMAS"


@pytest.fixture
def matrix() -> List[str]:
    text = [
        "ABCD",
        "EFGH",
        "IJKL",
        "MNOP",
    ]
    return text


@pytest.fixture
def matrix2() -> List[str]:
    text = [
        "AAXAAAAAXAAAAAAAAAXA",
        "AAAMAAAXMASAAAAAAMAA",
        "AAAAASAAAAAAAAAAAAAA",
        "AAAAASAASAAAAAASAAAA",
        "AAAMAAAAAAAAAAAAAAAA",
        "AAXAAAAAMAAAAAAAAMAA",
        "XMASAAAAXAAAAAASAMXA",
    ]
    return text


@pytest.fixture
def matrix3() -> List[str]:
    text = [
        "ABCDE",
        "FGHIJ",
        "KLMNO",
    ]
    return text


@pytest.mark.parametrize(
    ["pos", "vector", "expectation"],
    [
        [(0, 0), (+1, +0), "ABCD"],   # L.TOP -> R.TOP
        [(0, 0), (+1, +1), "AFKP"],   # L.TOP -> R.BTM
        [(0, 0), (+0, +1), "AEIM"],   # L.TOP -> L.BTM
        [(3, 0), (-1, +0), "DCBA"],  # R.TOP -> L.TOP
        [(3, 0), (-1, +1), "DGJM"],  # R.TOP -> L.BTM
        [(3, 0), (+0, +1), "DHLP"],  # R.TOP -> R.BTM
        [(0, 3), (+0, -1), "MIEA"],  # L.BTM -> L.TOP
        [(0, 3), (+1, -1), "MJGD"],  # L.BTM -> R.TOP
        [(0, 3), (+1, +0), "MNOP"],  # L.BTM -> R.BTM
        [(3, 3), (+0, -1), "PLHD"],  # R.BTM -> R.TOP
        [(3, 3), (-1, -1), "PKFA"],  # R.BTM -> L.TOP
        [(3, 3), (-1, +0), "PONM"],  # R.BTM -> L.BTM
    ],
)
def test_get_cross_section(
        pos: Tuple[int, int],
        vector: Tuple[int, int],
        expectation: str,
        matrix: List[str],
):
    result = aoc_04_1.get_cross_section(
        matrix,
        pos,
        vector,
        len(expectation),
    )
    assert result == expectation


@pytest.mark.parametrize(
    ["pos", "length", "expectation"],
    [
        [(0, 0), 2, ["AB", "AF", "AG"]]
    ]
)
def test_get_cross_sections(
        pos: Tuple[int, int],
        length: int,
        expectation: List[str],
        matrix3: List[str],
):
    cross_sections = aoc_04_1.get_cross_sections(
        matrix3,
        pos,
        length
    )
    assert cross_sections == expectation


def test_count_occurrences(matrix2: List[str]):
    result = aoc_04_1.count_occurrences(matrix2, "XMAS")
    assert result == 9


def test_main():
    puzzle_name = aoc.PuzzleName(
        day=4,
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
