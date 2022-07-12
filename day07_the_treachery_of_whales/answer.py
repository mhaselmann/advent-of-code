import argparse
from pathlib import Path


def read_input_file(path: Path) -> list[int]:
    with open(path) as f:
        input = f.readline()  # only read first line
    return list(map(int, input.split(",")))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - Day 7: The Treachery of Whales")
    parser.add_argument("-i", help="Input file path")
    args = parser.parse_args()
    path = Path(args.i) if args.i else Path("example_input.txt")
    assert path.exists()

    initial_hor_pos = read_input_file(path)
    print(initial_hor_pos)
