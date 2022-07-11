import argparse
from pathlib import Path


def read_input_file(path: Path) -> list[int]:
    with open(path) as f:
        input = f.readline()  # only read first line
    return list(map(int, input.split(",")))


def simulate_lanternfishes(
    initial_state: list[int], days: int, timer_reset: int = 6, new_lanternfish_timer: int = 8
) -> list[int]:
    state = initial_state.copy()
    for _ in range(days):
        new_lanternfishes = [new_lanternfish_timer] * state.count(0)
        state = [x - 1 if x > 0 else timer_reset for x in state] + new_lanternfishes
    return state


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - Day 6: Lanternfishes")
    parser.add_argument("-i", help="Input file path")
    parser.add_argument("-d", help="Simulate d days")
    args = parser.parse_args()
    path = Path(args.i) if args.i else Path("input.txt")
    days = int(args.d) if args.d else 80
    assert path.exists()

    state = read_input_file(path)
    state = simulate_lanternfishes(state, days)
    print(f"Answer part 1 (#lanternfishes after {days} days): {len(state)}")
