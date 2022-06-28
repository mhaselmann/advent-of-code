import argparse
from pathlib import Path


def hm_larger_than_previous(path: Path, sliding_window_size: int) -> int:
    answer = 0
    previous_depth = None
    current_depth = None
    sliding_window = []
    with open(path) as file:
        for line in file:
            # update sliding window and maintain trim if sliding_window_size is exceeded
            sliding_window.append(int(line))
            if len(sliding_window) > sliding_window_size:
                del sliding_window[0]
            assert len(sliding_window) <= sliding_window_size

            # compute current_depth if sliding_window has reached target size
            if len(sliding_window) == sliding_window_size:
                current_depth = sum(sliding_window)

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
    parser.add_argument("-s", default=3, help="Size of averaging sliding window")
    args = parser.parse_args()
    path = Path(args.i) if args.i else Path("input.txt")
    assert path.exists()
    sliding_window_size = int(args.s)

    answer = hm_larger_than_previous(path, sliding_window_size)
    print(
        f"Considering sums of a {sliding_window_size}-measurement sliding window. How many measurements are larger than the previous measurement?: {answer}"
    )
