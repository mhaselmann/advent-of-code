import argparse
from pathlib import Path
from collections import defaultdict


def read_input_file(path: Path) -> list[int]:
    with open(path) as f:
        input = f.readline()  # only read first line
    return list(map(int, input.split(",")))


class LanternfishSimulator:
    def __init__(
        self, initial_state: list[int], timer_reset: int = 6, new_lanternfish_timer: int = 8
    ):
        self._timer_reset = timer_reset
        self._new_lf_timer = new_lanternfish_timer
        self._max_timer = max(timer_reset, new_lanternfish_timer)
        self.state = {timer: initial_state.count(timer) for timer in range(self._max_timer + 1)}
        self.day = 0

    def simulate(self, days: int):
        self.day += days
        for _ in range(days):
            n_resets = self.state[0]
            self.state = {
                t: self.state[t + 1] if t < self._max_timer else n_resets
                for t in self.state.keys()
            }
            self.state[self._timer_reset] += n_resets

    def __len__(self):
        return sum(self.state.values())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - Day 6: Lanternfishes")
    parser.add_argument("-i", help="Input file path")
    parser.add_argument("-d", help="Simulate d days")
    args = parser.parse_args()
    path = Path(args.i) if args.i else Path("input.txt")
    days = int(args.d) if args.d else 80
    assert path.exists()

    state = read_input_file(path)
    simulator = LanternfishSimulator(state)
    simulator.simulate(days=days)

    print(f"Number of lanternfishes after {simulator.day} days: {len(simulator)}")
