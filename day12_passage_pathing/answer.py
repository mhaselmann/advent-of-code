import argparse
from pathlib import Path

from collections import defaultdict


def parse_input(path) -> tuple[dict[str, list[str]], list[str]]:
    graph = defaultdict(lambda: list())
    with open(path) as f:
        for line in f:
            node0, node1 = line.strip("\n").split("-")
            graph[node0].append(node1)
            if node0 != "start" and node1 != "end":
                graph[node1].append(node0)
    return graph


def find_all_paths(graph: dict[str, list[str]], start: str = "start", path: list[str] = []):
    path = path + [start]
    if start == "end":
        return [path]
    paths = list()
    for node in graph[start]:
        if node.isupper() or node not in path:
            new_paths = find_all_paths(graph, node, path)
            for new_path in new_paths:
                paths.append(new_path)
            # print(start, node, new_paths, paths)
    return paths


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - Day 12: Passage Pathing")
    parser.add_argument("-i", help="Input file path")
    args = parser.parse_args()
    path = Path(args.i) if args.i else Path("example_input.txt")
    assert path.exists()

    graph = parse_input(path)
    print(graph)

    paths = find_all_paths(graph)
    print("Results: ", paths)
