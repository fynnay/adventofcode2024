import pytest
import aoc


@pytest.mark.parametrize(
    [
        "input_value",
        "expected_result",
    ],
    [
        [
            "aoc_01_1",
            aoc.PuzzleName(
                day=1,
                part=1,
                base="aoc",
            )
        ],
        [
            "xmas_02_2",
            aoc.PuzzleName(
                day=2,
                part=2,
                base="xmas",
            )
        ],
        [
            "santa-123-0",
            aoc.PuzzleName(
                day=123,
                part=0,
                base="santa",
                delimiter="-",
            )
        ],
    ]
)
def test_parse(input_value, expected_result):
    result = aoc.PuzzleName.parse(input_value)
    assert result == expected_result
