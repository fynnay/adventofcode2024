from pathlib import Path


class Locations:
    ROOT = Path(__file__).parent.parent.parent
    INPUT = ROOT / "input"

    @classmethod
    def get_input_file(cls, file_name: str):
        return cls.INPUT / file_name
