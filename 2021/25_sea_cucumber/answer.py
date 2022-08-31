import argparse
from ast import parse
import copy
from pathlib import Path

import numpy as np


def parse_input(file_path: Path) -> np.ndarray:
    items = []
    with open(file_path) as f:
        for line in f:
            row_int = line.strip().replace(".", "0").replace(">", "1").replace("v", "2")
            items.append([int(c) for c in row_int])
    return np.array(items, dtype=np.uint8)


def step_east(items: np.ndarray) -> np.ndarray:
    free = items == 0
    east = items == 1
    desired = np.roll(east, 1)
    print("HERE")
    print(east.astype(np.uint8))
    print(desired.astype(np.uint8))
    print("\n")
    accepted = np.logical_and(desired, free)
    rejected = np.logical_and(desired, ~accepted)
    rejected = np.roll(rejected, -1)
    new_east = np.logical_or(accepted, rejected)
    new_items = np.zeros(items.shape, dtype=np.uint8)
    new_items[new_east > 0] = 1
    new_items[items == 2] = 2
    return new_items


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - Day 25: Sea cucumber")
    parser.add_argument("-i", help="Input file path")
    args = parser.parse_args()
    file_path = Path(args.i) if args.i else Path("example_input.txt")
    assert file_path.exists()

    array = parse_input(file_path)
    print(array)

    print(step_east(array))
