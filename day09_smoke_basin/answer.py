import argparse
import math
from pathlib import Path

import numpy as np
from numpy import ndarray
from scipy.ndimage import minimum_filter


def parse_input_file(path: Path) -> ndarray:
    rows = list()
    with open(path) as f:
        for line in f:
            rows.append([int(x) for x in line if x.isnumeric()])
    return np.array(rows, dtype=np.uint8)


def get_nearest_neighbor_locations(
    row: int, col: int, shape: tuple[int, int]
) -> tuple[list[int], list[int]]:  # list of rows, list of columns
    nn_rows, nn_cols = [row - 1, row + 1, row, row], [col, col, col - 1, col + 1]
    for idx in reversed(range(len(nn_rows))):
        if nn_rows[idx] < 0:
            del nn_rows[idx]
            del nn_cols[idx]
        elif nn_rows[idx] > shape[0] - 1:
            del nn_rows[idx]
            del nn_cols[idx]
        elif nn_cols[idx] < 0:
            del nn_rows[idx]
            del nn_cols[idx]
        elif nn_cols[idx] > shape[1] - 1:
            del nn_rows[idx]
            del nn_cols[idx]
    return nn_rows, nn_cols


def get_basins(height_map: ndarray, local_minima: ndarray) -> dict[tuple[int, int], ndarray]:
    """
    inputs:
    height_map ... numpy array of type np.uint8
    local_minima .. numpy array of type bool indicating the location of local minima (4-conn)
    output:
    dict[point of local minima, numpy arra of type bool indicating the basin]
    """

    def flow_upward_to_nearest_neighbors(
        basin: ndarray, flow_front_locs: tuple[list[int], list[int]]
    ) -> ndarray:
        for row, col in zip(*flow_front_locs):
            # for row, col in flow_front_locs:
            point = height_map[row, col]
            # go through all neighboring points
            nn_rows, nn_cols = get_nearest_neighbor_locations(row=row, col=col, shape=basin.shape)
            nn_points = height_map[nn_rows, nn_cols]
            higher = np.logical_and(nn_points > point, nn_points < 9)  # >= ??
            nn_rows = [r for r, higher in zip(nn_rows, higher) if higher]
            nn_cols = [r for r, higher in zip(nn_cols, higher) if higher]
            basin[nn_rows, nn_cols] = True
            if len(nn_rows):
                basin = flow_upward_to_nearest_neighbors(basin, (nn_rows, nn_cols))
        return basin

    basins = dict()
    local_minima_locations = np.where(local_minima)
    for row, col in zip(*local_minima_locations):
        basins[(row, col)] = np.zeros(height_map.shape, bool)
        basins[(row, col)][row, col] = True
        flow_upward_to_nearest_neighbors(basin=basins[(row, col)], flow_front_locs=([row], [col]))
    return basins


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - Day 7: The Treachery of Whales")
    parser.add_argument("-i", help="Input file path")
    args = parser.parse_args()
    path = Path(args.i) if args.i else Path("example_input.txt")
    assert path.exists()

    height_map = parse_input_file(path)

    # Part 1
    footprint = np.array([[False, True, False], [True, False, True], [False, True, False]], bool)
    min_filtered = minimum_filter(height_map, mode="mirror", footprint=footprint)
    local_minima = height_map < min_filtered
    local_minima_sum = (height_map + 1)[local_minima].sum()
    print(f"Answer part 1 - Sum of local minima of height map: {local_minima_sum}")

    # Part 2
    basins = get_basins(height_map, local_minima)
    basins_size = {k: v.sum() for k, v in basins.items()}
    basins_size = {k: v for k, v in sorted(basins_size.items(), key=lambda x: x[1])[::-1]}
    summed_size_of_3_largest_basin = math.prod(list(basins_size.values())[:3])
    print(f"Answer part 2 - Sum of size of 3 largest basins: {summed_size_of_3_largest_basin}")
