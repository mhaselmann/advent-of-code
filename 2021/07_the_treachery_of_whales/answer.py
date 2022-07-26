import argparse
from pathlib import Path
from typing import Callable


def read_input_file(path: Path) -> list[int]:
    with open(path) as f:
        input = f.readline()  # only read first line
    return list(map(int, input.split(",")))


def alignment_cost_part1(init_positions: list[int], alignment_position: int) -> int:
    return sum([abs(i - alignment_position) for i in init_positions])


def triangular_number(n: int) -> int:
    return int(n * (n + 1) / 2)


def alignment_cost_part2(init_positions: list[int], alignment_position: int) -> int:
    # pos_delta=[0, 1, 2, 3, 4, 5 ...] --> cost=[0, 1, 3, 6, 10, 15]  --> triangular number :)
    return sum([triangular_number(abs(i - alignment_position)) for i in init_positions])


def optimize_alignment_naive(cost_f: Callable, init_positions: list[int]) -> tuple[int, int]:
    """
    Optimize alignment cost function by trying out all values between min and max position
    Returns: Tuple[alignment_position, cost]
    """
    min_pos, max_pos = min(init_positions), max(init_positions)
    costs: dict[int, int] = dict()  # dict[alignment_pos, cost]
    for pos in range(min_pos, max_pos + 1):
        costs[pos] = cost_f(init_positions, pos)
    return min(costs.items(), key=lambda x: x[1])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - Day 7: The Treachery of Whales")
    parser.add_argument("-i", help="Input file path")
    args = parser.parse_args()
    path = Path(args.i) if args.i else Path("example_input.txt")
    assert path.exists()

    init_positions = read_input_file(path)
    alignment_pos, cost = optimize_alignment_naive(alignment_cost_part1, init_positions)
    print(f"Optimum Part1: Alignment position {alignment_pos}. Required fuel: {cost}")

    alignment_pos, cost = optimize_alignment_naive(alignment_cost_part2, init_positions)
    print(f"Optimum Part2: Alignment position {alignment_pos}. Required fuel: {cost}")
