import argparse
from pathlib import Path

from numpy import ndarray
import numpy as np


def parse_input_file(path: Path) -> ndarray:
    rows = list()
    with open(path) as f:
        for line in f:
            rows.append([int(x) for x in line if x.isnumeric()])
    return np.array(rows, dtype=np.uint8)


def get_nearest_neighbors_8c(
    row: int, col: int, shape: tuple[int, int]
) -> tuple[list[int], list[int]]:
    rows_cols = [
        (r, c)
        for r in range(row - 1, row + 2)
        for c in range(col - 1, col + 2)
        if r >= 0 and r < shape[0] and c >= 0 and c < shape[1] and not (r == row and c == col)
    ]
    return tuple(zip(*rows_cols))  # output can be used for indexing in numpy array


def step(energy_level_map: ndarray, flash_thres: int = 10):
    energy_level_map += 1
    flashes = np.where(energy_level_map >= flash_thres)
    while len(flashes[0]):
        for row, col in zip(*flashes):
            energy_level_map[row, col] = 0
            r, c = get_nearest_neighbors_8c(row, col, energy_level_map.shape)
            energy_level_map[r, c] = np.sign(energy_level_map[r, c]) * (energy_level_map[r, c] + 1)
            flashes = np.where(energy_level_map >= flash_thres)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - Day 11: Dumbo Octopus")
    parser.add_argument("-i", help="Input file path")
    args = parser.parse_args()
    path = Path(args.i) if args.i else Path("example_input.txt")
    assert path.exists()

    energy_level_map = parse_input_file(path)
    n_flashes = 0
    for _ in range(100):
        step(energy_level_map)
        n_flashes += (energy_level_map == 0).sum()
    print(f"Answer Part 1: Number of flashes: {n_flashes}")
