import argparse
from dataclasses import dataclass
from heapq import heappush, heappop
from pathlib import Path
import sys
import time
from typing import Callable, Optional

import numpy as np

sys.setrecursionlimit(2000)


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


def incr_array(array: np.ndarray, incr: int = 1, min_val: int = 1, max_val: int = 9) -> np.ndarray:
    new_array = array.copy()
    for _ in range(incr):
        new_array = new_array + 1
        new_array[new_array > max_val] = min_val
    return new_array


def get_array_mxn(array: np.ndarray, m: int, n: int):
    array_5x5 = np.concatenate([incr_array(array, i) for i in range(m)], axis=0)
    return np.concatenate([incr_array(array_5x5, i) for i in range(n)], axis=1)


def get_unvisited_neighbors(row: int, col: int, visited: np.ndarray) -> list[tuple[int, int]]:
    neighbors = [(row + 1, col), (row, col + 1), (row - 1, col), (row, col - 1)]
    for idx in reversed(range(4)):
        if neighbors[idx][0] < 0:
            neighbors.pop(idx)
        elif neighbors[idx][0] > visited.shape[0] - 1:
            neighbors.pop(idx)
        elif neighbors[idx][1] < 0:
            neighbors.pop(idx)
        elif neighbors[idx][1] > visited.shape[1] - 1:
            neighbors.pop(idx)
        elif visited[neighbors[idx][0], neighbors[idx][1]]:
            neighbors.pop(idx)
    return neighbors


def resolve_negative_indices(ind: tuple[int, ...], shape: tuple[int, ...]) -> tuple[int, ...]:
    return tuple([shape[d] + ind[d] if ind[d] < 0 else ind[d] for d in range(len(ind))])


def find_shortest_path_cost(
    weights: np.ndarray, start: tuple[int, int] = (0, 0), end: tuple[int, int] = (-1, -1)
) -> Optional[int]:
    """
    Dijkstras algorithm for searching the shortest path's cost
    """
    start = resolve_negative_indices(start, weights.shape)
    end = resolve_negative_indices(end, weights.shape)
    costs = 4294967295 * np.ones(weights.shape, np.uint32)
    costs[start[0], start[1]] = 0  # except for start node which is 0
    visited = np.zeros(weights.shape, bool)
    pq = []  # priority queue
    heappush(pq, (costs[start[0], start[1]], start))
    while len(pq):
        cost, node = heappop(pq)
        if node == end:
            return costs[node[0], node[1]]
        cost = costs[node[0], node[1]]
        visited[start[0], start[1]] = True
        for nb in get_unvisited_neighbors(*node, visited):
            new_nb_cost = cost + weights[nb[0], nb[1]]
            if new_nb_cost < costs[nb[0], nb[1]]:
                costs[nb[0], nb[1]] = new_nb_cost
                heappush(pq, (new_nb_cost, nb))
    print("Error: path not found", node)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - Day 15: Chiton")
    parser.add_argument("-i", help="Input file path")
    args = parser.parse_args()
    file_path = Path(args.i) if args.i else Path("example_input.txt")
    assert file_path.exists()

    weights = parse_input_file(file_path)

    t0 = time.time()
    cost = find_shortest_path_cost(weights)
    print(f"Answer part1 after {time.time() - t0}s: Shortest path's cost: {cost}")

    t0 = time.time()
    cost = find_shortest_path_cost(get_array_mxn(weights, 5, 5))
    print(f"Answer part2 after {time.time() - t0}s: Shortest path's cost: {cost}")
