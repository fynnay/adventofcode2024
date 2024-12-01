import re
from dataclasses import dataclass


@dataclass
class PuzzleName:
    day: int
    part: int
    base: str = "aoc"
    delimiter: str = "_"

    @classmethod
    def parse(cls, text: str) -> "PuzzleName":
        """
        Builds a PuzzleName from the given text
        """
        pattern = re.compile(r"(?P<base>\w+)_(?P<day>\d+)_(?P<part>\d+)")
        match = pattern.match(text)
        if not match:
            raise ValueError(f"Failed to get PuzzleName from '{text}'")

        base = match.group("base")
        day = int(match.group("day"))
        part = int(match.group("part"))

        return cls(
            base=base,
            day=day,
            part=part,
        )

    def build(self) -> str:
        base = self.base
        day = f"{self.day:02}"
        part = f"{self.part:01}"
        file_name = f"{self.delimiter.join([base, day, part])}"
        return file_name
