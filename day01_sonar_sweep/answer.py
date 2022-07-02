import argparse
from pathlib import Path


def hm_larger_than_previous(path: Path, sliding_window_size: int) -> int:
    # initialize and read out depths
    answer = 0
    current_depth = None
    previous_depth = None
    with open(path) as f:
        depths = list(map(int, f.readlines()))

    for idx, depth in enumerate(depths):
        # compute current_depth if sliding_window has reached target size
        window_start_idx = idx - (sliding_window_size - 1)
        if window_start_idx >= 0:
            current_depth = sum(depths[window_start_idx : idx + 1])

        # increment answer and update previous depth
        if previous_depth is not None and current_depth > previous_depth:
            answer += 1
        if current_depth is not None:
            previous_depth = current_depth
    return answer


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="How many measurements are larger than the previous measurement?"
    )
    parser.add_argument("-i", help="Input file path")
    args = parser.parse_args()
    path = Path(args.i) if args.i else Path("input.txt")
    assert path.exists()

    answer_part1 = hm_larger_than_previous(path, 1)
    print(f"How many measurements are larger than the previous measurement?: {answer_part1}")

    answer_part2 = hm_larger_than_previous(path, 3)
    print(
        f"Considering sums of a three-measurement sliding window."
        f" How many measurements are larger than the previous measurement?: {answer_part2}"
    )
