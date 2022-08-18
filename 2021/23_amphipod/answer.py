import argparse
import copy
from multiprocessing.sharedctypes import Value
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
        self.c = []
        self.c.append(cave0)
        self.c.append(cave1)
        self.c.append(cave2)
        self.c.append(cave3)
        self.h = hallway

    def __repr__(self):
        if len(self.c[0]) == 2:
            text = f"""
                #############
                #{self.h[0]}{self.h[1]}.{self.h[3]}.{self.h[5]}.{self.h[7]}.{self.h[9]}{self.h[10]}#
                ###{self.c[0][0]}#{self.c[1][0]}#{self.c[2][0]}#{self.c[3][0]}###
                  #{self.c[0][1]}#{self.c[1][1]}#{self.c[2][1]}#{self.c[3][1]}#
                  #########"""
        elif len(self.c[0]) == 4:
            text = f"""
                #############
                #{self.h[0]}{self.h[1]}.{self.h[3]}.{self.h[5]}.{self.h[7]}.{self.h[9]}{self.h[10]}#
                ###{self.c[0][0]}#{self.c[1][0]}#{self.c[2][0]}#{self.c[3][0]}###
                  #{self.c[0][1]}#{self.c[1][1]}#{self.c[2][1]}#{self.c[3][1]}#
                  #{self.c[0][2]}#{self.c[1][2]}#{self.c[2][2]}#{self.c[3][2]}#
                  #{self.c[0][3]}#{self.c[1][3]}#{self.c[2][3]}#{self.c[3][3]}#
                  #########"""
        else:
            raise NotImplementedError(len(self.c[0]), self.c[0])
        return text

    def __eq__(self, other: "State"):
        if self.h != other.h:
            return False
        for self_cave, other_cave in zip(self.c, other.c):
            if self_cave != other_cave:
                return False
        return True

    def __hash__(self):
        return hash(tuple(tuple(c) for c in self.c) + tuple(self.h))

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

    def is_state_valid(self) -> bool:
        """
        for debugging
        """
        for cave_idx, c in enumerate(self.c):
            last_place_occupied = True
            for pl, type_ in reversed(list(enumerate(c))):
                if type_ != "." and not last_place_occupied:
                    raise Exception(cave_idx, c)
                if type_ == ".":
                    last_place_occupied = False


class Node:
    def __init__(
        self,
        state: State,
        parent_state: State | None = None,
        step: int = 0,
        cost: int = 0,
    ):
        self.state = state
        self.parent_state = parent_state
        self.step = step
        self.cost = cost

        self.target_order = ["A", "B", "C", "D"]
        self.step_cost_per_type = {"A": 1, "B": 10, "C": 100, "D": 1000}
        self.type_to_cave = {cave: idx for idx, cave in enumerate(self.target_order)}

    def __repr__(self):
        return f"{self.state} ... {self.cost} \n"

    def is_finished(self) -> bool:
        for cave, type_ in zip(self.state.c, self.target_order):
            if cave != [type_, type_]:
                return False
        return True

    def _are_caves_entry_ready(self) -> list[int | None]:
        caves_entry_ready = []
        for c, targ_type in zip(self.state.c, self.target_order):
            caves_entry_ready.append(None)
            for pl, type_ in enumerate(c):
                if type_ == ".":
                    caves_entry_ready[-1] = pl
                elif type_ != targ_type:
                    caves_entry_ready[-1] = None
                    break
        return caves_entry_ready

    def _explore_hallway(
        self,
        incomplete_starting_node: "Node",
        cave_idx: int,
        cave_start_pos: int,
        item_type: str,
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
                new = copy.deepcopy(incomplete_starting_node)
                new.state.h[h_idx] = item_type
                new.step += 1
                new.cost += (cave_start_pos + distance + 2) * self.step_cost_per_type[item_type]
                new.parent_state = copy.deepcopy(self.state)
                new_nodes.append(new)

        # go rightwards
        for distance, h_idx in enumerate(range(h_idx_start + 1, 11)):
            if self.state.h[h_idx] is None:
                continue
            elif self.state.h[h_idx] != ".":
                break
            else:
                new = copy.deepcopy(incomplete_starting_node)
                new.state.h[h_idx] = item_type
                new.step += 1
                new.cost += (cave_start_pos + distance + 2) * self.step_cost_per_type[item_type]
                new.parent_state = copy.deepcopy(self.state)
                new_nodes.append(new)
        return new_nodes

    def get_next_possible_nodes(self) -> list["Node"]:
        caves_entry_ready = self._are_caves_entry_ready()

        # start from caves directly looking for target caves
        for cave_idx, c in enumerate(self.state.c):
            if caves_entry_ready[cave_idx] is not None:
                continue
            for place, type_ in enumerate(c):
                if type_ != ".":
                    target_cave_idx = self.type_to_cave[type_]
                    target_cave_pos = caves_entry_ready[target_cave_idx]
                    if target_cave_pos is None:
                        break
                    hallway_dist = self.state.distance_to_cave(target_cave_idx, cave_idx * 2 + 2)
                    if hallway_dist is None:
                        break
                    next_node = copy.deepcopy(self)
                    next_node.step += 1
                    next_node.parent_state = copy.deepcopy(self.state)
                    next_node.cost += (
                        place + 1 + hallway_dist + target_cave_pos + 1
                    ) * self.step_cost_per_type[type_]
                    next_node.state.c[cave_idx][place] = "."
                    next_node.state.c[target_cave_idx][target_cave_pos] = type_
                    return [next_node]

        # start from hallway
        for h_idx, type_ in enumerate(self.state.h):
            if type_ in [".", None]:
                continue
            cave_idx = self.type_to_cave[type_]
            sc = self.step_cost_per_type[self.target_order[cave_idx]]
            dist_to_cave = self.state.distance_to_cave(cave_idx, h_idx)
            if caves_entry_ready[cave_idx] is not None and dist_to_cave:
                new_state = copy.deepcopy(self)
                new_state.state.h[h_idx] = "."
                new_state.step += 1
                new_state.cost += dist_to_cave * sc
                new_state.parent_state = copy.deepcopy(self.state)
                for place, place_type in reversed(list(enumerate(self.state.c[cave_idx]))):
                    if place_type == ".":
                        new_state.state.c[cave_idx][place] = type_
                        new_state.cost += (place + 1) * sc
                        break
                return [new_state]

        next_nodes = list()
        # start from caves
        for cave_idx, c in enumerate(self.state.c):
            if caves_entry_ready[cave_idx]:
                continue
            for pl, type_ in enumerate(c):
                if type_ != ".":
                    n = copy.deepcopy(self)
                    n.state.c[cave_idx][pl] = "."
                    [next_nodes.append(s) for s in self._explore_hallway(n, cave_idx, pl, type_)]
                    break

        next_nodes = sorted(next_nodes, key=lambda x: x.cost)

        return next_nodes


class Graph:
    def __init__(self, start_state: State, end_state: State | None = None):
        self.nodes: dict[State, Node] = {}
        self.best_cost = 10**6
        self.start_state = start_state
        self.end_state = end_state
        if self.end_state is None:
            self.end_state = State(
                cave0=["A"] * len(start_state.c[0]),
                cave1=["B"] * len(start_state.c[0]),
                cave2=["C"] * len(start_state.c[0]),
                cave3=["D"] * len(start_state.c[0]),
            )
        self.find_shortest_path()

    def find_shortest_path(self, start: Node | None = None):
        if start is None:
            start = Node(self.start_state)
        if start.state in self.nodes and start.cost >= self.nodes[start.state].cost:
            return
        # start.state.is_state_valid()
        self.nodes[start.state] = start
        if start.state == self.end_state:
            self.best_cost = start.cost
            self.end_state = start.state
            print(f"Current shortest path length: {self.best_cost}")
        else:
            for next_node in start.get_next_possible_nodes():
                if next_node.cost < self.best_cost:
                    self.find_shortest_path(next_node)

    def print_shortest_path(self):
        state = self.end_state
        path_traceback: list[Node] = [state]
        while state := self.nodes[state].parent_state:
            path_traceback.append(self.nodes[state])
        for node in reversed(path_traceback):
            print(f"{node}")
        print(f"\nShortest path length: {self.best_cost}")


def parse_input_file(file_path: Path) -> State:
    with open(file_path) as f:
        lines = f.readlines()
    cave0, cave1, cave2, cave3 = [], [], [], []
    for l in lines[2:]:
        if l[3] == "#":
            break
        cave0.append(l[3])
        cave1.append(l[5])
        cave2.append(l[7])
        cave3.append(l[9])
    hallway = [
        lines[1][1],
        lines[1][2],
        None,
        lines[1][4],
        None,
        lines[1][6],
        None,
        lines[1][8],
        None,
        lines[1][10],
        lines[1][11],
    ]
    return State(cave0, cave1, cave2, cave3, hallway)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - Day 23: Amphipod")
    parser.add_argument("-i", help="Input file path")
    args = parser.parse_args()
    file_path = Path(args.i) if args.i else Path("example_input.txt")
    assert file_path.exists()

    start_state = parse_input_file(file_path)
    print(f"Starting state: {start_state}")

    graph = Graph(start_state=start_state)
    graph.print_shortest_path()
