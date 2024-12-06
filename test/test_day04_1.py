from typing import List, Tuple

import pytest

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
    text = (
        "ABCD\n"
        "EFGH\n"
        "IJKL\n"
        "MNOP\n"
    )
    return text.split("\n")


@pytest.mark.parametrize(
    ["pos", "vector", "expectation"],
    [
        [(0, 0), (+1, +0), "ABCD"],   # L.TOP -> R.TOP
        [(0, 0), (+1, -1), "AFKP"],   # L.TOP -> R.BTM
        [(0, 0), (+0, -1), "AEIM"],   # L.TOP -> L.BTM
        [(3, 0), (-1, +0), "DCBA"],  # R.TOP -> L.TOP
        [(3, 0), (-1, -1), "DGJM"],  # R.TOP -> L.BTM
        [(3, 0), (+0, -1), "DHLP"],  # R.TOP -> R.BTM
        [(0, 3), (+0, +1), "MIEA"],  # L.BTM -> L.TOP
        [(0, 3), (+1, +1), "MJGD"],  # L.BTM -> R.TOP
        [(0, 3), (+1, +0), "MNOP"],  # L.BTM -> R.BTM
        [(3, 3), (+0, +1), "PLHD"],  # R.BTM -> R.TOP
        [(3, 3), (-1, +1), "PKFA"],  # R.BTM -> L.TOP
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
