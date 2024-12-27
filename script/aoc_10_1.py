from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from aoc import (
    PuzzleName,
    Dir,
)


VECTOR = tuple[int, int]
ELEVATION = int
MAP = list[list[ELEVATION]]


@dataclass
class Point:
    x: int
    y: int


@dataclass(frozen=True, eq=True)
class Node:
    point: Point
    elevation: int


class Direction(Enum):
    UP: VECTOR = (0, 1)
    DOWN: VECTOR = (0, -1)
    RIGHT: VECTOR = (1, 0)
    LEFT: VECTOR = (-1, 0)


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
                if not entry:
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
        return self._nodes[point.y][point.x]

    def step_up(self, node: Node, gain: ELEVATION) -> list[Node]:
        """
        Returns a list of Nodes, whose elevation is exactly `gain` higher than `node`

        Args:
            node: Find next step(s) from this node
            gain: Elevation of next node(s) should be this much higher
        """
        # TODO
        pass

    def steps_ups(self, node: Node, gain: ELEVATION, max_steps: int = 9):
        # TODO
        trails = []
        for _ in range(max_steps):
            nodes = self.step_up(node, gain)
            pass


@dataclass
class Trail:
    start: Point
    steps: list[list[Point]]


def get_input_values(file_path: Path) -> Map:
    with open(file_path, 'r') as file:
        lines = file.readlines()
        return Map.from_lines(lines)


def process(tmap: Map):
    """
    - Find all trail heads
    - From each head, find all routes that gradually lead to a 9, those are trails
    - Count the number of trails each trail head has to give it a score
    - Sum the score of all trail heads

    Args:
        tmap: The trail map in which to look for trails
    """
    trail_heads: list[Node] = []
    trails: list[Trail] = []

    for node in tmap.nodes:
        if node.elevation != 0:
            continue
        trail_heads.append(node)

    for head in trail_heads:
        steps = tmap.step_up(head, 1)


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
