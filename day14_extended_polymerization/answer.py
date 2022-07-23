import argparse
from collections import defaultdict
from pathlib import Path
from typing import Optional


InsertionRules = dict[str, Optional[str]]


def parse_input(file_path: Path) -> tuple[str, InsertionRules]:

    with open(file_path) as f:
        insertion_rules = defaultdict(lambda: "")
        for idx, line in enumerate(f):
            if idx == 0:
                polymer = line.strip("\n")
            elif "->" in line:
                pair, insertion = line.strip("\n").split(" -> ")
                insertion_rules[pair] = insertion
    return polymer, insertion_rules


def insert_into_polymer(polymer: str, insertion_rules: InsertionRules) -> str:
    for idx in reversed(range(len(polymer) - 1)):
        polymer = polymer[: idx + 1] + insertion_rules[polymer[idx : idx + 2]] + polymer[idx + 1 :]
    return polymer


class PolymerPairRepr:
    def __init__(self, polymer: str):
        self.start = polymer[0]
        self.end = polymer[-1]
        self.pair_occ = defaultdict(lambda: 0)
        for idx in range(len(polymer) - 1):
            self.pair_occ[polymer[idx : idx + 2]] += 1

    def insert(self, insertion_rules: InsertionRules, iters: int = 1):
        # get pair to 2 pair rules from insertion rules
        pair_to_pairs = {}
        for pair, insert in insertion_rules.items():
            pair_to_pairs[pair] = (pair[0] + insert, insert + pair[1])

        for _ in range(iters):
            new_pair_occ = defaultdict(lambda: 0)
            for pair, amount in self.pair_occ.items():
                new_pair0, new_pair1 = pair_to_pairs[pair]
                new_pair_occ[new_pair0] += amount
                new_pair_occ[new_pair1] += amount
            self.pair_occ = new_pair_occ

    def get_element_occ(self) -> dict[str, int]:
        element_occ = defaultdict(lambda: 0)
        for pair, occurances in self.pair_occ.items():
            element_occ[pair[0]] += occurances
            element_occ[pair[1]] += occurances

        # pairs are sharing each element with another pair except for start and end element
        element_occ[self.start] += 1
        element_occ[self.end] += 1
        for element, occurances in element_occ.items():
            # assert element_occ[element] % 2 == 0  # if number of elements is even
            element_occ[element] = int(element_occ[element] / 2)
        return element_occ

    def __str__(self):
        return str(self.pair_occ)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code - Day 14: Extended Polymerization"
    )
    parser.add_argument("-i", help="Input file path")
    args = parser.parse_args()
    file_path = Path(args.i) if args.i else Path("example_input.txt")
    assert file_path.exists()

    polymer, insertion_rules = parse_input(file_path)
    poly_pair_repr = PolymerPairRepr(polymer)

    # Part 1 (10 iterations)
    for it in range(10):
        polymer = insert_into_polymer(polymer, insertion_rules)
    element_occ = {e: polymer.count(e) for e in set(polymer)}
    print(f"Answer p1: {max(list(element_occ.values()))-min(list(element_occ.values()))}")

    # Part 2 (40 iterations)
    poly_pair_repr.insert(insertion_rules, iters=40)
    element_occ = poly_pair_repr.get_element_occ()
    print(f"Answer p2: {max(list(element_occ.values()))-min(list(element_occ.values()))}")
