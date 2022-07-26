import argparse
from pathlib import Path

import cv2
import numpy as np


Folds = list[tuple[str, int]]


def get_transp_paper(file_path: Path) -> tuple[np.ndarray, Folds]:
    # determine array size
    pts: list[tuple[int, int]] = []  # y, x
    folds: Folds = []  # y | x = #row | #col
    max_y, max_x = 0, 0
    with open(file_path) as f:
        for line in f:
            if "," in line:
                x, y = map(int, line.strip("\n").split(","))  # parse text line
                max_y, max_x = max(max_y, y), max(max_x, x)
                pts.append((y, x))
            elif "=" in line:
                axis, idx = line.strip("\n").split("=")
                folds.append((axis[-1], int(idx)))

    # create "transparent paper"
    transp_paper = np.zeros(shape=(max_y + 1, max_x + 1), dtype=bool)
    for pt in pts:
        transp_paper[pt[0], pt[1]] = True
    return transp_paper, folds


def fold_paper(paper: np.ndarray, folds: Folds):
    for axis, idx in folds:
        if axis == "y":
            paper = np.maximum(paper[:idx, :], np.flipud(paper[idx + 1 :, :]))
        elif axis == "x":
            paper = np.maximum(paper[:, :idx], np.fliplr(paper[:, idx + 1 :]))
    return paper


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - Day 13: Transparent Origami")
    parser.add_argument("-i", help="Input file path")
    args = parser.parse_args()
    file_path = Path(args.i) if args.i else Path("example_input.txt")
    assert file_path.exists()

    paper, folds = get_transp_paper(file_path)
    folded_paper = fold_paper(paper, [folds[0]])
    print(f"Answer part 1: # dots visible: {folded_paper.sum()}")

    folded_paper = fold_paper(paper, folds)
    cv2.imwrite("answer_p2_code.png", folded_paper.astype(np.uint8) * 255)
