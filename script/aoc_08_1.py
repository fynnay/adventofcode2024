"""
In particular, an anti node occurs at any point that is perfectly in line with two antennas of the same frequency -
but only when one of the antennas is twice as far away as the other. This means that for any pair of antennas with
the same frequency, there are two anti nodes, one on either side of them.

Antennas with different frequencies don't create anti nodes; A and a count as different frequencies.
However, anti nodes can occur at locations that contain antennas.

How many unique anti-nodes can be placed within the bounds of the map?
"""
import re
from pathlib import Path

from aoc import (
    PuzzleName,
    Dir,
)

# Custom types
POINT = tuple[int, int]
VECTOR = tuple[int, int]
NODE = str
MATRIX = list[list[NODE]]
ELEMENT = tuple[POINT, NODE]
LINE = list[ELEMENT]

PATTERN_ANTENNA = r"[a-zA-Z0-9]"
PATTERN_ANTI_NODE = r"#"
PATTERN_EMPTY_NODE = r"\."


def get_input_values(file_path: Path) -> MATRIX:
    values = []

    with open(file_path, 'r') as file:
        for line in file.readlines():
            if not line:
                continue
            entries = [_ for _ in line.strip("\n").strip(" ")]
            values.append(entries)

    return values


def show_matrix(
        matrix: MATRIX,
):
    """
    Shows the `matrix` on screen
    """
    for line in matrix:
        print("".join(line))


def get_antennas(matrix: MATRIX) -> list[ELEMENT]:
    """
    Returns a list of ELEMENTS for each ANTENNA in the MATRIX
    """
    elements: list[ELEMENT] = []

    for i, line in enumerate(matrix):
        for j, node in enumerate(line):
            match = re.match(PATTERN_ANTENNA, node)
            if not match:
                continue
            element = ((j, i), node)
            elements.append(element)

    return elements


def get_line(
        matrix: MATRIX,
        point: POINT,
        vector: VECTOR,
        length: int = None,
) -> LINE:
    """
    Returns a cross-section from the `matrix` at the `point` in the direction of the `vector`.
    If `length` is specified, limit the amount of returned points.
    """
    x, y = point
    vx, vy = vector
    circuit: LINE = []

    while True:
        if length is not None and len(circuit) >= length:
            break
        if x < 0 or y < 0:
            break
        try:
            entry = matrix[y][x]
        except IndexError:
            break
        circuit.append(((x, y), entry))
        x += vx
        y += vy

    return circuit


def find_resonant_circuits(circuits: list[LINE]) -> list[LINE]:
    """
    Returns a list of the circuits that have good vibrations
    """
    resonant_circuits = []

    for circuit in circuits:
        nodes = [_[1] for _ in circuit if re.search(_[1], PATTERN_EMPTY_NODE)]
        for _ in nodes:
            if nodes.count(_) > 1:
                resonant_circuits.append(circuit)
                break
        else:
            continue

    return resonant_circuits


def process(input_values: MATRIX) -> int:
    show_matrix(input_values)
    return len(input_values)


def main(file_path: Path | None = None):
    script_path = Path(__file__)
    puzzle_name = PuzzleName.parse(script_path.stem)
    file_path = file_path or Dir.build_file_path(
        Dir.INPUT,
        puzzle_name=PuzzleName(
            day=puzzle_name.day,
            part=puzzle_name.part,
        )
    )
    input_values = get_input_values(file_path)
    result = process(input_values)
    return result


if __name__ == "__main__":
    RESULT = main()
    print(f"Result: {RESULT}")
