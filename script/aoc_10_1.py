from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Generator, Iterator

from aoc import (
    PuzzleName,
    Dir,
)


VECTOR = tuple[int, int]
ELEVATION = int
MAP = list[list[ELEVATION]]
TRAIL = list[list["Node"]]


@dataclass(frozen=True, eq=True)
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
                point = Point(x, y)
                if entry.isnumeric():
                    elevation = int(entry)
                else:
                    elevation = -1
                node = Node(point, elevation)
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
            gain: ELEVATION
            ) -> Iterator[Node]:
        """
        Returns a list of Nodes, whose elevation is exactly `gain` higher than `node`

        Args:
            node: Find next step(s) from this node
            gain: Elevation of next node(s) should be this much higher
        """
        for direction in Direction:
            point = node.point + direction.value
            next_node = self.node_at(point)
            if not next_node:
                continue
            if next_node.elevation - node.elevation == gain:
                yield next_node

    def steps_up(
            self,
            node: Node,
            gain: ELEVATION,
            max_elevation: int = 9,
            ) -> Iterator[Node]:
        """
        Yields all nodes, that gain 1 elevation per step from the given `node`
        [
            [0,1,2,3],
            [0,1,2,3,4,5],
            [0,1,2,3,4,5,6,7,8,9],
        ]

        Args:
            node:
            gain:
            max_elevation:
        """
        if node.elevation == max_elevation:
            return
        directional_step = self.step_up(node, gain)
        for step in directional_step:
            yield from self.steps_up(step, gain, max_elevation=max_elevation)

    def get_trail_heads(self) -> Iterator[Node]:
        for node in self.nodes:
            if node.elevation != 0:
                continue
            yield node

    def build_trails(self, from_node: Node) -> dict[Node, Node or dict]:
        """
        Recursively adds possible trails from the given node.
        Trails may lead to the same peak.

        Returns:
            Dictionary of all possible trails
        """
        tree: dict[Node, Node or dict] = {}
        directions = self.step_up(from_node, 1)

        for direction in directions:
            trails = self.build_trails(direction)
            tree[direction] = trails

        return tree

    def find_peaks(
            self,
            node: Node,
            peak_elevation: int = 9,
            visited: set[Node] = None
    ) -> Iterator[Node]:
        """
        Yields Nodes at `peak_elevation` connected to `node`
        """
        visited = visited or set()
        directions = self.step_up(node, 1)
        for step in directions:
            # if step in visited:
            #     continue
            # visited.add(step)
            if step.elevation == peak_elevation:
                yield step
            else:
                yield from self.find_peaks(
                    step,
                    peak_elevation=peak_elevation,
                    visited=visited,
                )

def get_input_values(file_path: Path) -> Map:
    with open(file_path, 'r') as file:
        lines = file.readlines()
        return Map.from_lines(lines)



def process(tmap: Map) -> int:
    """
    - Find all trail heads
    - From each head, find all routes that gradually lead to a 9, those are trails
    - Count the number of trails each trail head has to give it a score
    - Sum the score of all trail heads

    Args:
        tmap: The trail map in which to look for trails
    """
    trail_heads = tmap.get_trail_heads()
    all_peaks: list[set[Node]] = []

    for head in trail_heads:
        peaks = set(tmap.find_peaks(head))
        all_peaks.append(peaks)

    trail_scores = []

    for trail_head in all_peaks:
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
