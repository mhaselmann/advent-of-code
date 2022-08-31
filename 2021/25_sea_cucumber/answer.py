import argparse
from ast import parse
import copy
from pathlib import Path

import torch
from torch import Tensor


def parse_input(file_path: Path) -> Tensor:
    items = []
    with open(file_path) as f:
        for line in f:
            row_int = line.strip().replace(".", "0").replace(">", "1").replace("v", "2")
            items.append([int(c) for c in row_int])
    return torch.tensor(items, dtype=torch.uint8)


def step_east(items: Tensor) -> Tensor:
    free = items == 0
    east = items == 1
    desired = torch.roll(east, 1, 1)
    accepted = torch.logical_and(desired, free)
    rejected = torch.logical_and(desired, ~accepted)
    rejected = torch.roll(rejected, -1, 1)
    new_east = torch.logical_or(accepted, rejected)
    new_items = torch.zeros(items.shape, dtype=torch.uint8)
    new_items[new_east > 0] = 1
    new_items[items == 2] = 2
    return new_items


def step_south(items: Tensor) -> Tensor:
    free = items == 0
    south = items == 2
    desired = torch.roll(south, 1, 0)
    accepted = torch.logical_and(desired, free)
    rejected = torch.logical_and(desired, ~accepted)
    rejected = torch.roll(rejected, -1, 0)
    new_south = torch.logical_or(accepted, rejected)
    new_items = torch.zeros(items.shape, dtype=torch.uint8)
    new_items[items == 1] = 1
    new_items[new_south > 0] = 2
    return new_items


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - Day 25: Sea cucumber")
    parser.add_argument("-i", help="Input file path")
    args = parser.parse_args()
    file_path = Path(args.i) if args.i else Path("example_input.txt")
    assert file_path.exists()

    array = parse_input(file_path)
    print(array)
    for idx in range(10000):
        array_ = array.clone()
        array = step_east(array)
        array = step_south(array)
        if torch.equal(array, array_):
            print(array)
            print(f"No change after {idx + 1} steps")
            break
