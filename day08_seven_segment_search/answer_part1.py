import argparse
from pathlib import Path


def parse_input_file(path: Path) -> dict[tuple[str], tuple[str]]:
    displays = dict()  # dict[unique_signal_pattern, 4-digit-output]
    with open(path) as f:
        for line in f:
            unique_signal_pattern, four_digit_output = line.split("|")
            displays[tuple(unique_signal_pattern.split())] = tuple(four_digit_output.split())
    return displays


def count_1s_4s_7s(displays: dict[tuple[str], tuple[str]]) -> int:
    number = 0
    for four_digit_output in displays.values():
        for digit in four_digit_output:
            if len(digit) in [2, 3, 4, 7]:
                number += 1
    return number


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - Day 7: The Treachery of Whales")
    parser.add_argument("-i", help="Input file path")
    args = parser.parse_args()
    path = Path(args.i) if args.i else Path("example_input.txt")
    assert path.exists()

    displays = parse_input_file(path)
    n_1s_4s_7s = count_1s_4s_7s(displays)
    print(f"Part1: Number of digits 1, 4, 7: {n_1s_4s_7s}")
