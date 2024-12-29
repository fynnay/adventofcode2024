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

    def build_trail(self, previous_node: Node, next_node: Node or Iterator, tree: dict[Node, Node or dict] = None):
        tree = tree or {}
        tree.setdefault(previous_node, {})
        if isinstance(next_node, Node):
            tree[previous_node] = next_node
        else:
            tree[previous_node] = self.build_trail(previous_node, next_node, tree=tree)

        return tree

    def get_trails(self, head: Node) -> list[list[list[Node]]]:
        """
        Each head may exponentially grow into a large number of directions with each step.
        Keep track of each step in a separate list for each direction.
        Lastly, consolidate all unique trails, that lead to a peak to make
        clean lists of possible routes to take to each peak.
        The first item of each trail will be a single step followed by
        one or more lists of further steps.
        [
          head, [step, [...]],
        ]
        """
        # From this point, several directions may be possible
        directions = self.steps_up(head, 1, max_elevation=9)
        trails = [head]

        # Store each step
        for step in directions:
            trails.append(self.get_trails(step))
        return trails


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
    trail_heads = list(tmap.get_trail_heads())
    all_trails: list[TRAIL] = []

    for head in trail_heads:
        trails = tmap.get_trails(head)
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
