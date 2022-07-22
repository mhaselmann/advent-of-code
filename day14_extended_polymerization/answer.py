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


def insert_polymer(polymer: str, insertion_rules: InsertionRules) -> str:
    for idx in reversed(range(len(polymer) - 1)):
        polymer = polymer[: idx + 1] + insertion_rules[polymer[idx : idx + 2]] + polymer[idx + 1 :]
    return polymer


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code - Day 14: Extended Polymerization"
    )
    parser.add_argument("-i", help="Input file path")
    args = parser.parse_args()
    file_path = Path(args.i) if args.i else Path("example_input.txt")
    assert file_path.exists()

    polymer, pair_insertion_rules = parse_input(file_path)
    print(polymer, pair_insertion_rules)

    for it in range(10):
        polymer = insert_polymer(polymer, pair_insertion_rules)
    element_occ = {e: polymer.count(e) for e in set(polymer)}
    print(f"Answer part 1: {max(list(element_occ.values()))-min(list(element_occ.values()))}")
