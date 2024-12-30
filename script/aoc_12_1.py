from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Iterator

from aoc import (
    PuzzleName,
    Dir,
)

@dataclass(frozen=True, eq=True)
class Point:
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)


@dataclass(frozen=True, eq=True)
class Node:
    point: Point
    plant: str


@dataclass
class Region:
    nodes: list[Node]
    plant: str

    @property
    def area(self) -> int:
        return len(self.nodes)



class Direction(Enum):
    UP = Point(0, 1)
    DOWN = Point(0, -1)
    RIGHT = Point(1, 0)
    LEFT = Point(-1, 0)


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
                point = Point(x, y)
                node = Node(point, entry)
                nodes_x.append(node)

            nodes_y.append(nodes_x)

        return cls(nodes_y)

    @property
    def nodes(self) -> list[Node]:
        for y in self._nodes:
            for x in y:
                yield x

    def node_at(self, point: Point):
        if point.x < 0 or point.y < 0:
            return None
        try:
            node = self._nodes[point.y][point.x]
        except IndexError:
            return None
        else:
            return node

    def step_up(
            self,
            node: Node,
            plant: str
    ) -> Iterator[Node]:
        """
        Returns a list of Nodes, whose elevation is exactly `gain` higher than `node`

        Args:
            node: Find next step(s) from this node
            plant: Elevation of next node(s) should be this much higher
        """
        for direction in Direction:
            point = node.point + direction.value
            next_node = self.node_at(point)
            if not next_node:
                continue
            if next_node.plant == plant:
                yield next_node


def get_input_values(file_path: Path):
    values = []

    with open(file_path, 'r') as file:
        for line in file.readlines():
            if not line:
                continue

    return values


def process(input_values):

    pass


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
