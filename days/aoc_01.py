from pathlib import Path

from aoc import utils


def get_input_values() -> tuple[list[int], list[int]]:
    file_name = f"{Path(__file__).stem}.txt"
    file_path = utils.Locations.get_input_file(file_name)
    values_left = []
    values_right = []
    with open(file_path, 'r') as file:
        for line in file.readlines():
            if not line:
                continue
            entry_left, entry_right = line.split("   ")
            value_left = int(entry_left)
            value_right = int(entry_right)
            values_left.append(value_left)
            values_right.append(value_right)
    return values_left, values_right


def process(values: tuple[list[int], list[int]]) -> list[int]:
    """
    Maybe the lists are only off by a small amount! To find out, pair up the numbers and measure how far apart they are. Pair up the smallest number in the left list with the smallest number in the right list, then the second-smallest left number with the second-smallest right number, and so on.

    Within each pair, figure out how far apart the two numbers are; you'll need to add up all of those distances. For example, if you pair up a 3 from the left list with a 7 from the right list, the distance apart is 4; if you pair up a 9 with a 3, the distance apart is 6.

    Args:
        values: The input values

    Returns:
        List of distances between input values
    """
    values_left, values_right = values
    distances = []
    # Get the smallest number of each list
    # Pop them from their lists
    # Get distance and add to distances
    # Continue until all items have been processed
    while True:
        if not values_left:
            break
        value_left = min(values_left)
        values_left.remove(value_left)
        value_right = min(values_right)
        values_right.remove(value_right)
        distance = abs(value_left - value_right)
        distances.append(distance)

    return distances


def main():
    input_values = get_input_values()
    distances = process(input_values)
    result = sum(distances)
    print(result)


if __name__ == "__main__":
    main()
