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
from typing import Iterable

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
RECTANGLE = ((int, int), (int, int))

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
            vector[0] if magnitude == 0 else vector[0] / magnitude,
            vector[0] if magnitude == 0 else vector[1] / magnitude,
        )

    return vector_normalized


def rounded(vector: VECTOR_NORMALIZED, precision: int = 6) -> VECTOR_NORMALIZED:
    """
    Returns the vector rounded to the amount of decimals specified by precision
    Args:
        vector: A (normalized) vector
        precision: The number of decimals to round to
    """
    multiplier = 10 * precision
    vector_rounded = (round(vector[0] * multiplier) / multiplier, round(vector[1] * multiplier) / multiplier)
    return vector_rounded


def process(input_values: MATRIX) -> int:
    show_matrix(input_values)
    return len(input_values)


def group_aligned_nodes(nodes: list[NODE]) -> set[frozenset[NODE]]:
    """
    Each node is added to a group of exactly 2 nodes that:

    - Are placed on a straight line
    - Are not interrupted by other frequencies
    - A node can be part of multiple groups, but two groups can't contain the exact same nodes

    Returns:
        For example:
        [
            {  # GROUP_1
                {((0,0), "a"), ((2, 2), "a")},
                {((0,0), "a"), ((0, 5), "a")},
            },
            {  # GROUP_2
                {...},
            }
        ]

    """
    groups = set()

    for node in nodes:
        frequency = node[1]

        # Get all other nodes' vector to this one
        nodes_similar: list[tuple[VECTOR_NORMALIZED, NODE]] = []
        nodes_others: list[tuple[VECTOR_NORMALIZED, NODE]] = []

        for node_2 in nodes:
            # Skip this node
            if node_2 == node:
                continue
            frequency_2 = node_2[1]
            vector = get_vector(node[0], node_2[0])
            vector_normalized = normalized(vector)
            if frequency_2 == frequency:
                nodes_similar.append((vector_normalized, node_2))
            else:
                nodes_others.append((vector_normalized, node_2))

        for node_similar in nodes_similar:
            vector_1 = node_similar[0]
            for node_other in nodes_others:
                vector_2 = node_other[0]
                # if rounded(vector_2) == rounded(vector_1):
                #     # Signal is interrupted by antenna with different frequency
                #     break
            else:
                # Register pair
                pair = frozenset([node, node_similar[1]])
                groups.add(pair)
                continue
            # break

    return groups


def place_anti_nodes(node_groups: Iterable[Iterable[NODE]]) -> set[NODE]:
    """
    Place 1 anti-node on the opposing sides of each node-group.

    To get the anti-node's position:

    - Get the vector from node_1 -> node_2
    - Add that vector to the point of node_2
    - Repeat for node_2 -> node_1

    Returns:
        Set of unique anti-nodes
    """
    anti_nodes: set[NODE] = set()

    for group in list(node_groups):
        _nodes = list(group)
        node_1 = _nodes[0]
        node_2 = _nodes[1]
        vector = get_vector(node_1[0], node_2[0])
        anti_node_1 = (
            (
                node_1[0][0] + vector[0],
                node_1[0][1] + vector[1],
            ),
            "#"
        )
        anti_node_2 = (
            (
                node_2[0][0] - vector[0],
                node_2[0][1] - vector[1],
            ),
            "#"
        )
        anti_nodes.add(anti_node_1)
        anti_nodes.add(anti_node_2)

    return anti_nodes


def filter_far_nodes(nodes: Iterable[NODE], bounds: RECTANGLE) -> list[NODE]:
    """
    Returns only the nodes whose position is within the bounds

    Args:
        nodes: The nodes
        bounds: ((min_x, min_y), (max_x, max_y))
    """
    nodes_filtered = []
    min_x, min_y = bounds[0]
    max_x, max_y = bounds[1]

    for node in nodes:
        x, y = node[0]
        if not min_x <= x <= max_x or not min_y <= y <= max_y:
            continue

        nodes_filtered.append(node)

    return nodes_filtered


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

    # Group antennas by frequency
    antennas_grouped = group_aligned_nodes(antennas)

    # Place anti-nodes
    anti_nodes = place_anti_nodes(antennas_grouped)

    # Filter out-of-bounds anti-nodes
    max_x = len(input_values[0]) - 1
    max_y = len(input_values) - 1
    anti_nodes_filtered = filter_far_nodes(anti_nodes, ((0, 0), (max_x, max_y)))

    return len(anti_nodes_filtered)


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
