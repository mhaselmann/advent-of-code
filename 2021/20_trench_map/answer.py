import argparse
import copy
from pathlib import Path

import numpy as np


ImgEnhAlgorithm = dict[np.ndarray, bool]


def np_to_tuple(np_ndarray: np.ndarray) -> tuple[tuple[bool, ...], ...]:
    return tuple(map(tuple, np_ndarray))


def parse_input_file(file_path: Path) -> tuple[ImgEnhAlgorithm, np.ndarray]:
    decode_line = lambda line: tuple(True if c == "#" else False for c in line)
    with open(file_path) as f:
        rows = list()
        for idx, line in enumerate(f):
            line = line.strip()
            if idx == 0:
                iea = decode_line(line)
            elif len(line):
                rows.append(decode_line(line))
    return {
        np_to_tuple(np.array(list(map(int, bin(i)[2:].zfill(9)))).reshape(3, 3) > 0): b
        for i, b in enumerate(iea)
    }, np.array(rows)


def enhance_image(
    img: np.ndarray, img_enh_algorithm: ImgEnhAlgorithm, iters: int = 2
) -> np.ndarray:
    zero_to_one = list(img_enh_algorithm.values())[0]
    for i in range(iters):
        cv = i % 2 > 0 and zero_to_one
        print("HERE", i, cv, iters)
        img = np.pad(img, [(3, 3), (3, 3)], mode="constant", constant_values=cv)
        img_enh = img.copy()
        for row in range(1, img.shape[0] - 1):
            for col in range(1, img.shape[1] - 1):
                img_enh[row, col] = img_enh_algorithm[
                    np_to_tuple(img[row - 1 : row + 2, col - 1 : col + 2])
                ]
        # remove zeros at corners
        for row in range(1, img_enh.shape[0] - 1):
            if np.sum(img_enh[row, :]) > 0:
                img_enh = img_enh[row:, :]
                break
        for row in reversed(range(1, img_enh.shape[0] - 1)):
            if np.sum(img_enh[row, :]):
                img_enh = img_enh[: row + 1, :]
                break
        for col in range(1, img_enh.shape[1] - 1):
            if np.sum(img_enh[:, col]):
                img_enh = img_enh[:, col:]
                break
        for col in reversed(range(1, img_enh.shape[1] - 1)):
            if np.sum(img_enh[:, col]):
                img_enh = img_enh[:, : col + 1]
                break
        img = img_enh.copy()
    return img_enh


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - Day 20: Trench map")
    parser.add_argument("-i", help="Input file path")
    args = parser.parse_args()
    file_path = Path(args.i) if args.i else Path("example_input.txt")
    assert file_path.exists()

    iea, img = parse_input_file(file_path)
    print(img.astype(np.uint8))
    img = enhance_image(img, iea, 2)
    print(img.astype(np.uint8))
    print(f"Answer part 1: How many pixels are lit up after 2 iterations: {img.sum()}")
