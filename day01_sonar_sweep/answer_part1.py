import argparse
from pathlib import Path


def hm_larger_than_previous(path: Path) -> int:
    answer = 0
    previous_depth = None
    with open(path) as file:
        for line in file:
            current_depth = int(line)
            if previous_depth is not None and current_depth > previous_depth:
                answer += 1
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

    answer = hm_larger_than_previous(path)
    print(f"How many measurements are larger than the previous measurement?: {answer}")
