import argparse
from pathlib import Path
import re

import numpy as np


def get_vent_map(path: Path, no_diag_lines: bool = False) -> np.ndarray:
    # determine necessary map size
    vent_lines_hv, vent_lines_diag = [], []
    max_y, max_x = 0, 0
    with open(path) as f:
        for line in f:
            x0, y0, x1, y1 = map(int, re.split(" -> |,", line))
            if y0 == y1 or x0 == x1:  # consider hor. and ver. vent_lines_hv
                max_y, max_x = max(max_y, y0, y1), max(max_x, x0, x1)
                if y0 + x0 < y1 + x1:
                    vent_lines_hv.append(((y0, y1), (x0, x1)))
                else:
                    vent_lines_hv.append(((y1, y0), (x1, x0)))
            elif not no_diag_lines:  # consider vertical lines
                max_y, max_x = max(max_y, y0, y1), max(max_x, x0, x1)
                y_sign, x_sign = np.sign(y1 - y0), np.sign(x1 - x0)
                vent_line_ys, vent_line_xs = [], []
                for idx in range(abs(y1 - y0) + 1):
                    vent_line_ys.append(y0 + y_sign * idx)
                    vent_line_xs.append(x0 + x_sign * idx)
                vent_lines_diag.append((vent_line_ys, vent_line_xs))

    # create vent map
    vent_map = np.zeros(shape=(max_y + 1, max_x + 1), dtype=np.uint8)
    for vl in vent_lines_hv:
        vent_map[vl[0][0] : vl[0][1] + 1, vl[1][0] : vl[1][1] + 1] += 1
    for vl in vent_lines_diag:
        vent_map[tuple(vl)] += 1

    return vent_map


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - Day 5: Hydrothermal Venture")
    parser.add_argument("-i", help="Input file path")
    args = parser.parse_args()
    path = Path(args.i) if args.i else Path("input.txt")
    assert path.exists()
    vent_map = get_vent_map(path, no_diag_lines=True)
    vent_overlap = vent_map >= 2
    print(f"Answer part 1 (no diagonal lines): {vent_overlap.sum()}")

    vent_map = get_vent_map(path)
    vent_overlap = vent_map >= 2
    print(f"Answer part 2 (with diagonal lines): {vent_overlap.sum()}")
