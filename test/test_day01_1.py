import sys
from importlib import util
import aoc


def test_day01_1():
    puzzle_name = aoc.PuzzleName(
        day=1,
        part=1,
    )
    puzzle_name_text = puzzle_name.build()
    input_file = aoc.utils.Dir.build_file_path(
        aoc.utils.Dir.INPUT,
        puzzle_name,
    )
    python_file = aoc.utils.Dir.build_file_path(
        aoc.utils.Dir.SCRIPT,
        puzzle_name,
    )
    spec = util.spec_from_file_location(puzzle_name_text, python_file)
    module = util.module_from_spec(spec)
    sys.modules[puzzle_name_text] = module  # Optional: add the module to sys.modules
    spec.loader.exec_module(module)

    result = module.main(input_file)
    correct_result = 1873376

    assert result == correct_result
