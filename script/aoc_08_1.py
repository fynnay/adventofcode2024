"""
In particular, an anti node occurs at any point that is perfectly in line with two antennas of the same frequency -
but only when one of the antennas is twice as far away as the other. This means that for any pair of antennas with
the same frequency, there are two anti nodes, one on either side of them.

Antennas with different frequencies don't create anti nodes; A and a count as different frequencies.
However, anti nodes can occur at locations that contain antennas.

How many unique anti-nodes can be placed within the bounds of the map?
"""
import math
import re
from pathlib import Path

from aoc import (
    PuzzleName,
    Dir,
)

# Custom types
POINT = tuple[int, int]
VECTOR = tuple[int, int]
VECTOR_NORMALIZED = tuple[float, float]
FREQUENCY = str
MATRIX = list[list[FREQUENCY]]
NODE = tuple[POINT, FREQUENCY]

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


def get_antennas(matrix: MATRIX) -> list[NODE]:
    """
    Returns a list of NODE in the MATRIX for each FREQUENCY matching the PATTERN_ANTENNA
    """
    nodes: list[NODE] = []

    for i, line in enumerate(matrix):
        for j, frequency in enumerate(line):
            match = re.match(PATTERN_ANTENNA, frequency)
            if not match:
                continue
            node = ((j, i), frequency)
            nodes.append(node)

    return nodes


def get_line(
        matrix: MATRIX,
        point: POINT,
        vector: VECTOR,
        length: int = None,
) -> list[NODE]:
    """
    Returns a cross-section from the `matrix` at the `point` in the direction of the `vector`.
    If `length` is specified, limit the amount of returned points.
    """
    x, y = point
    vx, vy = vector
    circuit: list[NODE] = []

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


def find_resonant_circuits(circuits: list[list[NODE]]) -> list[list[NODE]]:
    """
    Returns a list of the circuits that have good vibrations
    """
    resonant_circuits = []

    for circuit in circuits:
        frequencies = [_[1] for _ in circuit if re.search(_[1], PATTERN_EMPTY_NODE)]
        for _ in frequencies:
            if frequencies.count(_) > 1:
                resonant_circuits.append(circuit)
                break
        else:
            continue

    return resonant_circuits


def get_vector(point_1: POINT, point_2: POINT) -> VECTOR:
    """
    Returns the vector of point_1 to point_2
    """
    vector = (
        point_1[0] - point_2[0],
        point_1[1] - point_2[1],
    )
    return vector


def normalized(vector: VECTOR, scaled: bool = False) -> VECTOR_NORMALIZED:
    """
    Normalize the given vector either by square root or max absolute value
    """
    if scaled:
        max_abs = max(abs(vector[0]), abs(vector[1]))
        vector_normalized = [
            vector[0] if max_abs == 0 else vector[0] / max_abs,
            vector[1] if max_abs == 0 else vector[1] / max_abs,
        ]
    else:
        magnitude = math.sqrt(
            math.pow(
                vector[0],
                2
            ) + math.pow(
                vector[1],
                2
            )
        )
        vector_normalized = (
            vector[0] / magnitude,
            vector[1] / magnitude,
        )

    return vector_normalized


def rounded(vector: VECTOR_NORMALIZED) -> VECTOR:
    return int(round(vector[0])), int(round(vector[1]))


def process(input_values: MATRIX) -> int:
    show_matrix(input_values)
    return len(input_values)


def process_2(input_values: MATRIX) -> int:
    """
    - Get all antenna points
    - Find antennas with same FREQUENCY
    - Find antennas with direct line of sight
    - Place anti-nodes on either side, within bounds of map
    - Count number of anti-nodes within bounds of map
    """
    # Get all antennas
    antennas = get_antennas(input_values)

    # Group antennas by FREQUENCY
    antenna_groups: dict[str, list[NODE]] = {}
    for _ in antennas:
        frequency = _[1]
        antenna_groups.setdefault(frequency, [])
        antenna_groups[frequency].append(_)

    # Find antennas with matching frequency
    for frequency, group in antenna_groups.items():
        for node in group:
            point_1 = node[0]
            other_antennas = [_ for _ in group if _ != node]
            for antenna_2 in other_antennas:
                point_2 = antenna_2[0]
                vector = get_vector(point_1, point_2)
                vector_normalized = normalized(vector)
                vector_rounded = rounded(vector_normalized)
                # Check whether there are any obstructions in line of sight
                line = get_line(
                    input_values,
                    point_2,
                    vector_rounded,
                )
                print(vector, vector_normalized)

    # TODO: Place anti-nodes
    return len(antenna_groups)


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
    result = process_2(input_values)
    return result


if __name__ == "__main__":
    RESULT = main()
    print(f"Result: {RESULT}")
