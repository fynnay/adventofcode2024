from dataclasses import dataclass, field
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


@dataclass(eq=True)
class Region:
    plant: str
    points: list[Point] = field(default_factory=list)
    perimeter: int = -1
    border: list[Point] = field(default_factory=list)

    @property
    def area(self) -> int:
        """
        Returns the amount of nodes in this region
        """
        return len(self.points)

    @property
    def cost(self) -> int:
        """
        The area * perimeter = cost
        """
        return self.area * self.perimeter

    def point_at(self, point: Point) -> Node or None:
        """
        Returns the node if one is found at the `point` or None.
        """
        for _ in self.points:
            if _ == point:
                return _

    def calculate_perimeter(self):
        """
        Calculates the length of nodes around this area.
        """
        self.border = []
        # Count points around each node, that are not part of this Region
        for point in self.points:
            for direction in Direction:
                other_point = point + direction.value
                other = self.point_at(other_point)
                if other is None:
                    self.border.append(other_point)
        self.perimeter = len(self.border)


class Direction(Enum):
    UP = Point(0, 1)
    DOWN = Point(0, -1)
    RIGHT = Point(1, 0)
    LEFT = Point(-1, 0)


@dataclass
class Land:
    _nodes: list[list[Node]]

    @classmethod
    def from_lines(cls, lines: list[str]) -> "Land":
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

    def next_node(
            self,
            node: Node,
    ) -> Iterator[Node]:
        """
        Returns a list of Nodes, whose elevation is exactly `gain` higher than `node`

        Args:
            node: Find next step(s) from this node
        """
        for direction in Direction:
            point = node.point + direction.value
            next_node = self.node_at(point)
            if not next_node:
                continue
            if next_node.plant == node.plant:
                yield next_node

    def get_connected_nodes(
            self,
            node: Node,
            visited: set[Node] = None
            ) -> Iterator[Node]:
        visited = visited or {node}
        yield node
        for step in self.next_node(node):
            if step in visited:
                continue
            visited.add(step)
            yield from self.get_connected_nodes(step, visited=visited)

    def find_regions(self) -> list[Region]:
        regions = []

        processed = set()
        for node in self.nodes:
            if node in processed:
                continue
            connected_nodes = list(self.get_connected_nodes(node))
            region = Region(node.plant, points=[_.point for _ in connected_nodes])
            regions.append(region)
            processed.update(connected_nodes)

        return regions

def get_input_values(file_path: Path):
    values = []

    with open(file_path, 'r') as file:
        for line in file.readlines():
            if not line:
                continue
            values.append([_ for _ in line.strip("\n") if _])

    return values


def process(input_values):
    land = Land.from_lines(input_values)
    # Get regions
    regions: list[Region] = land.find_regions()
    # Calculate border
    for region in regions:
        region.calculate_perimeter()
    total_cost = sum([_.cost for _ in regions])
    return total_cost


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
