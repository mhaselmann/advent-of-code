import argparse
from dataclasses import dataclass
from pathlib import Path
import re

import numpy as np


@dataclass
class TargetArea:
    x0: int
    x1: int
    y0: int
    y1: int

    def is_point_inside(self, pt: tuple[int, int]) -> bool:  # x,y point
        return pt[0] >= self.x0 and pt[0] <= self.x1 and pt[1] >= self.y0 and pt[1] <= self.y1

    def is_shot_missed(self, pos: tuple[int, int]):
        return pos[1] < self.y0

    def __str__(self):
        return f"x= {self.x0}..{self.x1},  y= {self.y0}..{self.y1}"


def parse_input_file(file_path: Path) -> TargetArea:
    with open(file_path) as f:
        line = f.readline()
    _, xr, _, yr = re.split("=|,", line)
    return TargetArea(*map(int, xr.split("..")), *map(int, yr.split("..")))


class TrickShotSimulator:
    def __init__(self, target_area: TargetArea):
        self.target_area = target_area

    def simulate(
        self,
        init_velocity: list[int, int],
        start_pos: list[int, int] = (0, 0),
        max_t: int = 100000,
    ):
        vel = init_velocity
        pos = start_pos
        for t in range(max_t):
            pos = [sum(x) for x in zip(pos, vel)]  # step 1,2
            if vel[0] > 0:
                vel[0] -= 1  # step 3 (drag)
            vel[1] -= 1  # step 4 (gravity)
            if self.target_area.is_point_inside(pos):
                return pos
            if self.target_area.is_shot_missed(pos):
                return
        raise ValueError(f"max_t too low: {pos[1]}{self.target_area.y0}")

    def grid_search(self):
        x_vels, y_vels = np.meshgrid(
            range(self.target_area.x1 + 5), range(self.target_area.y0, -self.target_area.y0)
        )
        hits = np.zeros(x_vels.shape, bool)
        for row in range(hits.shape[0]):
            for col in range(hits.shape[1]):
                hits[row, col] = self.simulate([x_vels[row, col], y_vels[row, col]])
        return hits


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - Day 17: Trick Shot")
    parser.add_argument("-i", help="Input file path")
    args = parser.parse_args()
    file_path = Path(args.i) if args.i else Path("example_input.txt")
    assert file_path.exists()

    target_area = parse_input_file(file_path)
    print(f"Answer part 1: Highest y position: {sum(range(-target_area.y0))}")

    trick_shot_sim = TrickShotSimulator(target_area)
    hits = trick_shot_sim.grid_search()
    print(f"Answer part 2: How many hitting initial velocities: {hits.sum()}")
