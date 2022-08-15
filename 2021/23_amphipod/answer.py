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

    def __repr__(self):
        text = f"""
               #############
               #{self.h[0]}{self.h[1]}.{self.h[3]}.{self.h[5]}.{self.h[7]}.{self.h[9]}{self.h[10]}#
               ###{self.c[0][0]}#{self.c[1][0]}#{self.c[2][0]}#{self.c[3][0]}###
                 #{self.c[0][1]}#{self.c[1][1]}#{self.c[2][1]}#{self.c[3][1]}#
                 #########"""
        return text

    def __eq__(self, other: "State"):
        if self.h != other.h:
            return False
        for self_cave, other_cave in zip(self.c, other.c):
            if self_cave != other_cave:
                return False
        return True

    def __hash__(self):
        return hash((tuple(c) for c in self.c) + tuple(self.h))

    def distance_to_cave(self, cave_idx: int, h_idx_start: int) -> int | None:
        """
        Returns distance to cave. If cave is not reachable (due to obstacles) return None
        """
        h_idx_end = cave_idx * 2 + 2
        if h_idx_start < h_idx_end:
            for distance, h_idx in enumerate(range(h_idx_start + 1, h_idx_end + 1)):
                if self.h[h_idx] not in [".", None]:
                    return None
        elif h_idx_start > h_idx_end:
            for distance, h_idx in enumerate(range(h_idx_start - 1, h_idx_end - 1, -1)):
                if self.h[h_idx] not in [".", None]:
                    return None
        return distance + 1


class Node:
    def __init__(
        self,
        state: State,
        parent_state: State | None = None,
        cost: int = 0,
    ):
        self.state = state
        self.parent_state = parent_state
        self.cost = cost

        self.target_order = ["A", "B", "C", "D"]
        self.step_cost_per_type = {"A": 1, "B": 10, "C": 100, "D": 1000}
        self.type_to_cave = {cave: idx for idx, cave in enumerate(self.target_order)}

    def __repr__(self):
        return f"{self.state}  {self.cost} \n"

    def is_finished(self) -> bool:
        for cave, type_ in zip(self.state.c, self.target_order):
            if cave != [type_, type_]:
                return False
        return True

    def _are_caves_entry_ready(self) -> list[bool]:
        caves_entry_ready = []
        for c, targ_type in zip(self.state.c, self.target_order):
            if c[0] == "." and c[1] in [".", targ_type] or c[0] == targ_type and c[1] == targ_type:
                caves_entry_ready.append(True)
            else:
                caves_entry_ready.append(False)
        return caves_entry_ready

    def _explore_hallway(
        self,
        incomplete_starting_node: "Node",
        cave_idx: int,
        item_type: str,
        cost_offset: int,
    ) -> list["Node"]:
        """
        Returns all possibles States from start_idx [2, 4, 6, 8]
        without colliding any other item in the hallway
        """
        assert cave_idx in range(4)
        h_idx_start = cave_idx * 2 + 2
        new_nodes: list["Node"] = []
        # go leftwards
        for distance, h_idx in enumerate(reversed(range(h_idx_start))):
            if self.state.h[h_idx] is None:
                continue
            elif self.state.h[h_idx] != ".":
                break
            else:
                new_node = copy.deepcopy(incomplete_starting_node)
                new_node.state.h[h_idx] = item_type
                new_node.cost += cost_offset + (distance + 1) * self.step_cost_per_type[item_type]
                new_nodes.append(new_node)
        # go rightwards
        for distance, h_idx in enumerate(range(h_idx_start + 1, 11)):
            if self.state.h[h_idx] is None:
                continue
            elif self.state.h[h_idx] != ".":
                break
            else:
                new_node = copy.deepcopy(incomplete_starting_node)
                new_node.state.h[h_idx] = item_type
                new_node.cost += cost_offset + (distance + 1) * self.step_cost_per_type[item_type]
                new_nodes.append(new_node)
        return new_nodes

    def get_next_possible_nodes(self) -> list["Node"]:
        next_nodes = list()
        caves_entry_ready = self._are_caves_entry_ready()

        # start from caves
        for cave_idx, c in enumerate(self.state.c):
            sc = self.step_cost_per_type[self.target_order[cave_idx]]
            if caves_entry_ready[cave_idx]:
                continue
            elif c[0] != ".":
                n = copy.deepcopy(self)
                n.state.c[cave_idx][0] = "."
                [next_nodes.append(s) for s in self._explore_hallway(n, cave_idx, c[0], 1 * sc)]
            elif c[1] != ".":
                n = copy.deepcopy(self)
                n.state.c[cave_idx][1] = "."
                [next_nodes.append(s) for s in self._explore_hallway(n, cave_idx, c[0], 2 * sc)]

        # start from hallway
        for h_idx, type_ in enumerate(self.state.h):
            if type_ in [".", None]:
                continue
            target_cave_idx = self.state.type_to_cave[type_]
            dist_to_cave = self.state.distance_to_cave(cave_idx=target_cave_idx, h_idx_start=h_idx)
            if caves_entry_ready[target_cave_idx] and dist_to_cave:
                new_node = copy.deepcopy(self)
                new_node.state.h[h_idx] = "."
                if self.c[target_cave_idx][1] == ".":
                    new_node.state.c[target_cave_idx][1] = type_
                elif self.c[target_cave_idx][0] == ".":
                    new_node.state.c[target_cave_idx][0] = type_
                else:
                    raise ValueError(f"Illegal node {new_node} {type_}")
                next_nodes.append(new_node)

        return next_nodes


class Graph:
    def __init__(self, starting_node: State):
        self.nodes = {starting_node: 0}


def parse_input_file(file_path: Path) -> State:
    with open(file_path) as f:
        l = f.readlines()
    return State(
        cave0=[l[2][3], l[3][3]],
        cave1=[l[2][5], l[3][5]],
        cave2=[l[2][7], l[3][7]],
        cave3=[l[2][9], l[3][9]],
        hallway=[
            l[1][1],
            l[1][2],
            None,
            l[1][4],
            None,
            l[1][6],
            None,
            l[1][8],
            None,
            l[1][10],
            l[1][11],
        ],
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
    print(state != state2, state == state2)
    next_nodes = Node(state).get_next_possible_nodes()
    for n in next_nodes:
        print(n)
