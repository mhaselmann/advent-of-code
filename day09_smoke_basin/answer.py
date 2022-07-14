import argparse
from pathlib import Path

import numpy as np
from scipy.ndimage import minimum_filter


def parse_input_file(path: Path) -> np.ndarray:
    rows = list()
    with open(path) as f:
        for line in f:
            rows.append([int(x) for x in line if x.isnumeric()])
    return np.array(rows, dtype=np.uint8)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - Day 7: The Treachery of Whales")
    parser.add_argument("-i", help="Input file path")
    args = parser.parse_args()
    path = Path(args.i) if args.i else Path("example_input.txt")
    assert path.exists()

    height_map = parse_input_file(path)
    footprint = np.array([[False, True, False], [True, False, True], [False, True, False]], bool)
    min_filtered = minimum_filter(height_map, mode="mirror", footprint=footprint)
    is_local_minima = height_map < min_filtered
    local_minima_sum = (height_map + 1)[is_local_minima].sum()

    print(f"Answer part 1 - Sum of local minima of height map: {local_minima_sum}")
