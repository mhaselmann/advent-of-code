import argparse
from pathlib import Path
import re
from typing import Optional

import numpy as np


def get_vent_map(path: Path) -> np.ndarray:
    # determine necessary map size
    vent_lines = []
    max_y, max_x = 0, 0
    with open(path) as f:
        for line in f:
            x0, y0, x1, y1 = map(int, re.split(" -> |,", line))
            if y0 == y1 or x0 == x1:  # consider hor. and ver. vent_lines only
                max_y, max_x = max(max_y, y0, y1), max(max_x, x0, x1)
                if y0 + x0 < y1 + x1:
                    vent_lines.append([[y0, x0], [y1, x1]])
                else:
                    vent_lines.append([[y1, x1], [y0, x0]])

    vent_map = np.zeros(shape=(max_y + 1, max_x + 1), dtype=np.uint8)
    for vl in vent_lines:
        vent_map[vl[0][0] : vl[1][0] + 1, vl[0][1] : vl[1][1] + 1] += 1

    return vent_map


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code Day 04: Giant Squid:")
    parser.add_argument("-i", help="Input file path")
    args = parser.parse_args()
    path = Path(args.i) if args.i else Path("input.txt")
    assert path.exists()
    vent_map = get_vent_map(path)
    vent_overlap = vent_map >= 2
    print(f"Answer part 1: {vent_overlap.sum()}")
