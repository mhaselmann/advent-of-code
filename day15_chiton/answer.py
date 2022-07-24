import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import numpy as np


Node = tuple[int, int]


@dataclass
class GraphPath:
    path: list[Node]
    weight: int = 0


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


def path_cond(node: Node, path: GraphPath) -> bool:
    return False if node in path.path else True


def path_cond_(node: Node, path: GraphPath) -> bool:
    return False if node in path.path else True


def find_all_paths(
    graph: np.ndarray,
    path_cond: Callable[[Node, GraphPath], bool],
    start: Node = [0, 0],
    path: GraphPath = GraphPath([]),
) -> list[GraphPath]:
    path = GraphPath(path=path.path + [start], weight=path.weight + graph[start[0], start[1]])
    if start == (graph.shape[0] - 1, graph.shape[1] - 1):
        return [path]
    paths = []
    neighbors = get_nearest_neighbor_locations(*start, shape=graph.shape)
    for neighbor in zip(*neighbors):
        if path_cond(node=neighbor, path=path):
            [paths.append(p) for p in find_all_paths(graph, path_cond, neighbor, path)]
    return paths


def get_minimum_path(paths: list[GraphPath]) -> GraphPath:
    return min(paths.items(), key=lambda x: x[1])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - Day 15: Chiton")
    parser.add_argument("-i", help="Input file path")
    args = parser.parse_args()
    file_path = Path(args.i) if args.i else Path("example_input.txt")
    assert file_path.exists()

    graph = parse_input_file(file_path)
    print(graph)

    paths = find_all_paths(graph=graph, path_cond=path_cond)
    minimum_path = min(paths, key=lambda x: x.weight)
    print(len(paths), minimum_path)
    print(f"Answer part1: Minimal risk path's risk: {minimum_path.weight}")
