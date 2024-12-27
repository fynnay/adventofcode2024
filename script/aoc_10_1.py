from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Generator

from aoc import (
    PuzzleName,
    Dir,
)


VECTOR = tuple[int, int]
ELEVATION = int
MAP = list[list[ELEVATION]]
TRAIL = list[list["Node"]]


@dataclass
class Point:
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

@dataclass(frozen=True, eq=True)
class Node:
    point: Point
    elevation: int


class Direction(Enum):
    UP: VECTOR = Point(0, 1)
    DOWN: VECTOR = Point(0, -1)
    RIGHT: VECTOR = Point(1, 0)
    LEFT: VECTOR = Point(-1, 0)


@dataclass
class Map:
    _nodes: list[list[Node]]

    @classmethod
    def from_lines(cls, lines: list[str]) -> "Map":
        nodes_y = []

        for y, line in enumerate(lines):
            nodes_x = []
            if not line:
                continue

            for x, entry in enumerate(line):
                if not entry.strip("."):
                    continue

                point = Point(x, y)
                node = Node(point, int(entry))
                nodes_x.append(node)

            nodes_y.append(nodes_x)

        return cls(nodes_y)

    @property
    def nodes(self) -> list[Node]:
        for y in self._nodes:
            for x in y:
                yield x

    def node_at(self, point: Point):
        try:
            node = self._nodes[point.y][point.x]
        except IndexError:
            return None
        else:
            return node

    def step_up(self, node: Node, gain: ELEVATION) -> list[Node]:
        """
        Returns a list of Nodes, whose elevation is exactly `gain` higher than `node`

        Args:
            node: Find next step(s) from this node
            gain: Elevation of next node(s) should be this much higher
        """
        steps = []

        for direction in Direction:
            point = node.point + direction.value
            next_node = self.node_at(point)
            if not next_node:
                continue
            if next_node.elevation - node.elevation == gain:
                steps.append(next_node)

        return steps

    def steps_ups(self, node: Node, gain: ELEVATION, max_elevation: int = 9):
        if node.elevation == max_elevation:
            return
        steps = self.step_up(node, gain)
        for step in steps:
            yield step
            yield from self.steps_ups(step, gain, max_elevation=max_elevation)


def get_input_values(file_path: Path) -> Map:
    with open(file_path, 'r') as file:
        lines = file.readlines()
        return Map.from_lines(lines)


def get_trail_heads(tmap: Map) -> Generator[Node, None, None]:
    for node in tmap.nodes:
        if node.elevation != 0:
            continue
        yield node


def get_trails(previous: Node, tmap: Map) -> list[TRAIL]:
    """
    """
    trails = tmap.steps_ups(previous, 1, max_elevation=9)

    for trail in trails:
        pass

    return trails


def process(tmap: Map) -> int:
    """
    - Find all trail heads
    - From each head, find all routes that gradually lead to a 9, those are trails
    - Count the number of trails each trail head has to give it a score
    - Sum the score of all trail heads

    Args:
        tmap: The trail map in which to look for trails
    """
    trail_heads = list(get_trail_heads(tmap))
    all_trails: list[TRAIL] = []

    for head in trail_heads:
        trails = get_trails(head, tmap)
        all_trails.append(trails)

    trail_scores = []

    for trail_head in all_trails:
        trail_scores.append(len(trail_head))

    trail_score = sum(trail_scores)

    return trail_score


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
    result = "I am result"
    return result


if __name__ == "__main__":
    RESULT = main()
    print(f"Result: {RESULT}")
