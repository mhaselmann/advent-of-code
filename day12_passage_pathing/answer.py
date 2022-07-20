import argparse
from pathlib import Path
from typing import Callable

from collections import defaultdict


def parse_input(file_path) -> dict[str, list[str]]:
    graph = defaultdict(lambda: list())
    with open(file_path) as f:
        for line in f:
            node0, node1 = line.strip("\n").split("-")
            if node1 == "start":
                node0, node1 = node1, node0
            graph[node0].append(node1)
            if node0 != "start" and node1 != "end":
                graph[node1].append(node0)
    return graph


def path_cond_part1(node: str, path: list[str]) -> bool:
    if node.isupper() or node not in path:
        return True


def path_cond_part2(node: str, path: list[str]) -> bool:
    if node.islower() and node in path:
        new_path = path + [node]
        occurances = {n: new_path.count(n) for n in new_path if n.islower()}
        if max(list(occurances.values())) > 2 or list(occurances.values()).count(2) > 1:
            return False
    return True


# Dijkstra's Algorithm  https://stackoverflow.com/questions/24471136/how-to-find-all-paths-between-two-graph-nodes
def find_all_paths(
    graph: dict[str, list[str]],
    path_cond: Callable,
    start: str = "start",
    path: list[str] = [],
) -> list[list[str]]:
    path = path + [start]
    if start == "end":
        return [path]
    paths = list()
    for node in graph[start]:
        if path_cond(node=node, path=path):
            [paths.append(p) for p in find_all_paths(graph, path_cond, node, path)]
    return paths


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - Day 12: Passage Pathing")
    parser.add_argument("-i", help="Input file path")
    args = parser.parse_args()
    file_path = Path(args.i) if args.i else Path("example_input.txt")
    assert file_path.exists()

    graph = parse_input(file_path)
    paths_part1 = find_all_paths(graph, path_cond_part1)
    print(f"Answer part 1: #Paths: {len(paths_part1)}")

    paths_part2 = find_all_paths(graph, path_cond_part2)
    print(f"Answer part 2: #Paths: {len(paths_part2)}")
