import argparse
import copy
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
        self.c = []
        self.c.append(cave0)
        self.c.append(cave1)
        self.c.append(cave2)
        self.c.append(cave3)
        self.h = hallway
        self.cost = cost
        self.target_order = ["A", "B", "C", "D"]
        self.target_item_type_to_cave = {cave: idx for idx, cave in enumerate(self.target_order)}

    def __repr__(self):
        text = f"""
               #############
               #{self.h[0]}{self.h[1]}.{self.h[3]}.{self.h[5]}.{self.h[7]}.{self.h[9]}{self.h[10]}#
               ###{self.c[0][0]}#{self.c[1][0]}#{self.c[2][0]}#{self.c[3][0]}###
                 #{self.c[0][1]}#{self.c[1][1]}#{self.c[2][1]}#{self.c[3][1]}#
                 #########\n"""
        return text

    def __eq__(self, other: "State"):
        if self.h != other.h:
            return False
        for self_cave, other_cave, type_ in zip(self.c, other.c, self.target_order):
            if self_cave != other_cave:
                return False
        return True

    def __ne__(self, other: "State"):
        return not self.__eq__(other)

    def is_finished(self) -> bool:
        for cave, type_ in zip(self.c, self.target_order):
            if cave != [type_, type_]:
                return False
        return True

    def _explore_hallway(
        self,
        incomplete_starting_state: "State",
        cave_idx: int,
        item_type: str,
        cost_offset: int,
    ) -> list["State"]:
        """
        Returns all possibles States from start_idx [2, 4, 6, 8]
        without colliding any other item in the hallway
        """
        assert cave_idx in range(4)
        assert cost_offset in [1, 2]
        h_idx_start = cave_idx * 2 + 2
        new_states: list["State"] = []
        # go leftwards
        for distance, h_idx in reversed(list(enumerate(range(h_idx_start)))):
            if self.h[h_idx] is None:
                continue
            elif self.h[h_idx] != ".":
                break
            else:
                new_state = copy.deepcopy(incomplete_starting_state)
                new_state.h[h_idx] = item_type
                new_state.cost += cost_offset + distance
                new_states.append(new_state)
        # go rightwards
        for distance, h_idx in enumerate(range(h_idx_start + 1, 11)):
            if self.h[h_idx] is None:
                continue
            elif self.h[h_idx] != ".":
                break
            else:
                new_state = copy.deepcopy(incomplete_starting_state)
                new_state.h[h_idx] = item_type
                new_state.cost += cost_offset + distance
                new_states.append(new_state)
        return new_states

    def are_caves_entry_ready(self) -> list[bool]:
        caves_entry_ready = []
        for c, targ_type in zip(self.c, self.target_order):
            if c[0] == "." and c[1] in [".", targ_type] or c[0] == targ_type and c[1] == targ_type:
                pass

    def get_next_possible_states(self) -> list["State"]:
        next_states = list()
        # start from caves
        for cave_idx, (c, targ_type) in enumerate(zip(self.c, self.target_order)):
            if c[0] == "." and c[1] in [".", targ_type] or c[0] == targ_type and c[1] == targ_type:
                continue
            elif c[0] != ".":
                incomplete_starting_state = copy.deepcopy(self)
                incomplete_starting_state.c[cave_idx][0] = "."
                next_states.append(
                    self._explore_hallway(incomplete_starting_state, cave_idx, c[0], 1)
                )
            elif c[1] != ".":
                incomplete_starting_state = copy.deepcopy(self)
                incomplete_starting_state.c[cave_idx][1] = "."
                next_states.append(
                    self._explore_hallway(incomplete_starting_state, cave_idx, c[1], 2)
                )
        # start from hallway
        for h_idx, type_ in enumerate(self.h):
            if type_ in [".", None]:
                continue
            target_cave_idx = self.target_item_type_to_cave[type_]

        return next_states


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
    next_states = state.get_next_possible_states()
    for s in next_states:
        print(s)
