from enum import Enum
from pathlib import Path
from .puzzle_name import PuzzleName


class Dir(Enum):
    ROOT = Path(__file__).parent.parent.parent
    SCRIPT = ROOT / "script"
    INPUT = ROOT / "input"

    @classmethod
    def build_file_name(cls, loc: "Dir", puzzle_name: PuzzleName):
        ext_lookup = {
            cls.SCRIPT: ".py",
            cls.INPUT: "",
        }
        stem = puzzle_name.build()
        return f"{stem}{ext_lookup[loc]}"

    @classmethod
    def build_file_path(cls, loc: "Dir", puzzle_name: PuzzleName):
        file_name = cls.build_file_name(loc, puzzle_name)
        file_path = loc.value / file_name
        return file_path
