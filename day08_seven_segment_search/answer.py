import argparse
from pathlib import Path
from typing import Iterable


def parse_input_file(path: Path) -> dict[tuple[str], tuple[str]]:
    displays = dict()  # dict[unique_signal_pattern, 4-digit-output]
    with open(path) as f:
        for line in f:
            unique_signal_pattern, four_digit7s_output = line.split("|")
            displays[tuple(unique_signal_pattern.split())] = tuple(four_digit7s_output.split())
    return displays


def count_1s_4s_7s(displays: dict[tuple[str], tuple[str]]) -> int:
    number = 0
    for four_digit7s_output in displays.values():
        for digit in four_digit7s_output:
            if len(digit) in [2, 3, 4, 7]:
                number += 1
    return number


class Digit7sDecoder:
    def __init__(self, unique_signal_pattern: tuple[str]):
        assert len(unique_signal_pattern) == 10
        # store each unique signal pattern digit in an alpabetically order
        self.usp = list("".join(sorted(digit7s)) for digit7s in unique_signal_pattern)

        self.digit7s_to_digit: dict[str, int] = dict()
        self.digit_to_digit7s: dict[int, str] = dict()
        self.matches = list()
        self.build_lookup_tables()

    def build_lookup_tables(self):
        self.usp_leftovers = self.usp.copy()
        # digit 1, 4, 7, 8 known from number of elements
        # digit 3 is a the one 5-segment digit that contains digit 1
        # digit 9 is a the one 6-segment digit that contains digit 4
        # digit 5 is a leftover 5-segment digit which is contained in digit 9
        # digit 2 is the last leftover 5-segment digit
        # digit 0 is a leftover 6-segment digit containing digit 1
        # digit 6 is the last leftover digit

        # digit 1, 4, 7, 8 known from number of elements
        match = [i for i, x in enumerate(self.usp) if len(x) == 2]
        self.store_decoding(digit=1, match=match)

        match = [i for i, x in enumerate(self.usp) if len(x) == 3]
        self.store_decoding(digit=7, match=match)

        match = [i for i, x in enumerate(self.usp) if len(x) == 4]
        self.store_decoding(digit=4, match=match)

        match = [i for i, x in enumerate(self.usp) if len(x) == 7]
        self.store_decoding(digit=8, match=match)

        # digit 3 is a the one 5-segment digit that contains digit 1
        match = [
            i
            for i, x in enumerate(self.usp)
            if len(x) == 5 and self.are_x_segments_subset_of_y(self.digit_to_digit7s[1], x)
        ]
        self.store_decoding(digit=3, match=match)

        # digit 9 is a the one 6-segment digit that contains digit 4
        match = [
            i
            for i, x in enumerate(self.usp)
            if len(x) == 6
            and i not in self.matches
            and self.are_x_segments_subset_of_y(self.digit_to_digit7s[4], x)
        ]
        self.store_decoding(digit=9, match=match)

        # digit 5 is a leftover 5-segment digit which is contained in digit 9
        match = [
            i
            for i, x in enumerate(self.usp)
            if len(x) == 5
            and i not in self.matches
            and self.are_x_segments_subset_of_y(x, self.digit_to_digit7s[9])
        ]
        self.store_decoding(digit=5, match=match)

        # digit 2 is the last leftover 5-segment digit
        match = [i for i, x in enumerate(self.usp) if len(x) == 5 and i not in self.matches]
        self.store_decoding(digit=2, match=match)

        # digit 0 is a leftover 6-segment digit containing digit 1
        match = [
            i
            for i, x in enumerate(self.usp)
            if len(x) == 6
            and i not in self.matches
            and self.are_x_segments_subset_of_y(self.digit_to_digit7s[1], x)
        ]
        self.store_decoding(digit=0, match=match)

        # digit 6 is the last leftover digit
        match = [i for i, x in enumerate(self.usp) if i not in self.matches]
        self.store_decoding(digit=6, match=match)

        assert len(self.matches) == 10

    def store_decoding(self, digit: int, match: list[int]):
        assert len(match) == 1
        self.digit7s_to_digit[self.usp[match[0]]] = digit
        self.digit_to_digit7s[digit] = self.usp[match[0]]
        self.matches.append(match[0])

    @staticmethod
    def are_x_segments_subset_of_y(x_digit7s: str, y_digit7s: str) -> bool:
        return all([y_digit7s.find(x_seg) >= 0 for x_seg in x_digit7s])

    def __call__(self, digits7s: Iterable[str]) -> int:
        digits = list()
        for digit7s in digits7s:
            digits.append(self.digit7s_to_digit["".join(sorted(digit7s))])
        return int("".join(map(str, digits)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - Day 7: The Treachery of Whales")
    parser.add_argument("-i", help="Input file path")
    args = parser.parse_args()
    path = Path(args.i) if args.i else Path("example_input.txt")
    assert path.exists()

    displays = parse_input_file(path)
    n_1s_4s_7s = count_1s_4s_7s(displays)
    print(f"Part1: Number of digits 1, 4, 7: {n_1s_4s_7s}")

    displays_sum = 0
    for usp, four_digit7s_output in displays.items():
        decoder = Digit7sDecoder(usp)
        displays_sum += decoder(digits7s=four_digit7s_output)

    print(f"Part2: Displays sum: {displays_sum}")
