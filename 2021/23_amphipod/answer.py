import argparse
from pathlib import Path


class State:
    def __init__(
        self,
        cave0: list[str],
        cave1: list[str],
        cave2: list[str],
        cave3: list[str],
        hallway: list[str | None] = [".", ".", None, ".", None, ".", None, ".", None, ".", "."],
        cost: int = 0,
    ):
        assert len(cave0) == 2
        assert len(cave1) == 2
        assert len(cave2) == 2
        assert len(cave3) == 2
        assert hallway[2] is None
        assert hallway[4] is None
        assert hallway[6] is None
        assert hallway[8] is None
        self.c0 = cave0
        self.c1 = cave1
        self.c2 = cave2
        self.c3 = cave3
        self.h = hallway
        self.cost = cost

    def __str__(self):
        text = f"""
               #############
               #{self.h[0]}{self.h[1]}.{self.h[3]}.{self.h[5]}.{self.h[7]}.{self.h[9]}{self.h[10]}#
               ###{self.c0[0]}#{self.c1[0]}#{self.c2[0]}#{self.c3[0]}###
                 #{self.c0[1]}#{self.c1[1]}#{self.c2[1]}#{self.c3[1]}#
                 #########"""
        return text

    def __eq__(self, other: "State"):
        if (
            self.c0 == other.c0
            and self.c1 == other.c1
            and self.c2 == other.c2
            and self.c3 == other.c3
            and self.h == other.h
        ):
            return True
        else:
            return False

    def __ne__(self, other: "State"):
        return not self.__eq__(other)

    def is_finished(self) -> bool:
        if (
            self.c0 == ["a", "a"]
            and self.c1 == ["b", "b"]
            and self.c2 == ["c", "c"]
            and self.c3 == ["d", "d"]
        ):
            return True
        else:
            return False

    def get_next_possible_states(self):
        pass


def parse_input_file(file_path: Path) -> State:
    with open(file_path) as f:
        lines = f.readlines()
    return State(
        cave0=[lines[2][3], lines[3][3]],
        cave1=[lines[2][5], lines[3][5]],
        cave2=[lines[2][7], lines[3][7]],
        cave3=[lines[2][9], lines[3][9]],
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - Day 23: Amphipod")
    parser.add_argument("-i", help="Input file path")
    args = parser.parse_args()
    file_path = Path(args.i) if args.i else Path("example_input.txt")
    assert file_path.exists()

    state = parse_input_file(file_path)
    state2 = parse_input_file(file_path)
    print(state)
    print(state == state2)
