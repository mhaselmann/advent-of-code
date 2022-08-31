import argparse
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


def step(items: Tensor, east: bool) -> Tensor:
    moving_idx = 1 if east else 2
    frozen_idx = 2 if east else 1
    axis = 1 if east else 0

    free = items == 0
    moving = items == moving_idx
    desired = torch.roll(moving, 1, axis)
    accepted = torch.logical_and(desired, free)
    rejected = torch.logical_and(desired, ~accepted)
    rejected = torch.roll(rejected, -1, axis)
    new_moving = torch.logical_or(accepted, rejected)
    new_items = torch.zeros(items.shape, dtype=torch.uint8)
    new_items[items == frozen_idx] = frozen_idx
    new_items[new_moving > 0] = moving_idx
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
        array = step(array, east=True)
        array = step(array, east=False)
        if torch.equal(array, array_):
            print(array)
            print(f"No change after {idx + 1} steps")
            break
