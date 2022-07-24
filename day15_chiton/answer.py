import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional

import numpy as np


Node = tuple[int, int]


@dataclass
class GraphPath:
    path: list[Node]
    weight_sum: int = 0


def parse_input_file(path: Path) -> np.ndarray:
    rows = list()
    with open(path) as f:
        for line in f:
            rows.append([int(x) for x in line if x.isnumeric()])
    return np.array(rows, dtype=np.uint8)


def get_nearest_neighbor_locations(
    row: int, col: int, shape: tuple[int, int]
) -> tuple[list[int], list[int]]:  # list of rows, list of columns
    # priotize down and left moves to priotize short paths
    nn_rows, nn_cols = [row + 1, row, row - 1, row], [col, col + 1, col, col - 1]
    for idx in reversed(range(len(nn_rows))):
        if nn_rows[idx] < 0:
            nn_rows.pop(idx), nn_cols.pop(idx)
        elif nn_rows[idx] > shape[0] - 1:
            nn_rows.pop(idx), nn_cols.pop(idx)
        elif nn_cols[idx] < 0:
            nn_rows.pop(idx), nn_cols.pop(idx)
        elif nn_cols[idx] > shape[1] - 1:
            nn_rows.pop(idx), nn_cols.pop(idx)
    return nn_rows, nn_cols


class MinimumPathFinder:
    def __init__(self, graph: np.ndarray):
        self.weight_sum: Optional[int] = None
        self.path: Optional[list[Node]] = None
        self.__search(graph)

    def __path_cond(self, node: Node, path: GraphPath) -> bool:
        return False if node in path.path else True

    def __search(
        self,
        graph: np.ndarray,
        start: Node = [0, 0],
        path: GraphPath = GraphPath([]),
    ) -> list[GraphPath]:
        path = GraphPath(path.path + [start], path.weight_sum + graph[start[0], start[1]])
        # cancel path traversing if weight is above min_path_weight
        dist_to_end = graph.shape[0] - 1 - start[0] + graph.shape[1] - 1 - start[1]
        if self.weight_sum is not None and path.weight_sum + dist_to_end >= self.weight_sum:
            return []
        if start == (graph.shape[0] - 1, graph.shape[1] - 1):
            print("HERE", path.weight_sum, self.weight_sum)
            self.weight_sum = path.weight_sum
            self.path
            return [path]
        paths = []
        neighbors = get_nearest_neighbor_locations(*start, shape=graph.shape)
        for neighbor in zip(*neighbors):
            if self.__path_cond(node=neighbor, path=path):
                [paths.append(p) for p in self.__search(graph, neighbor, path)]
        return paths


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - Day 15: Chiton")
    parser.add_argument("-i", help="Input file path")
    args = parser.parse_args()
    file_path = Path(args.i) if args.i else Path("example_input.txt")
    assert file_path.exists()

    graph = parse_input_file(file_path)
    print(graph)

    min_path_finder = MinimumPathFinder(graph)
    # minimum_path = min(paths, key=lambda x: x.weight)
    print(min_path_finder.weight_sum)
    print(f"Answer part1: Minimal risk path's risk: {min_path_finder.weight_sum-1}")
