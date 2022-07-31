import argparse
import copy
from math import copysign
from pathlib import Path
from typing import Iterator


Point, Vector, Orientation = tuple[int, ...], tuple[int, ...], tuple[int, int, int]
PointVectors = dict[Point, list[Vector]]  # {starting point: vector to all other points}
Views = dict[int, list[Point]]


def parse_input_file(file_path: Path) -> Views:
    views = dict()
    with open(file_path) as f:
        for line in f:
            line = line.strip()
            if line[:3] == "---":
                key = int(line.split()[2])
                views[key] = list()
            elif len(line):
                views[key].append(tuple(map(int, line.split(","))))
    return views


def add(x_: Point | Vector, y_: Point | Vector) -> Point | Vector:
    return tuple([x + y for x, y in zip(x_, y_)])


def subtract(x_: Point | Vector, y_: Point | Vector) -> Point | Vector:
    return tuple([x - y for x, y in zip(x_, y_)])


def get_all_point_to_point_vectors(points=list[Point]) -> list[PointVectors]:
    points = sorted(points)  # sort all points
    pv = dict()
    for idx in range(len(points)):
        other_points = copy.deepcopy(points)
        root_point = other_points.pop(idx)
        pv[root_point] = list()
        for other_point in other_points:
            pv[root_point].append(subtract(other_point, root_point))
    return pv


# https://stackoverflow.com/questions/16452383/how-to-get-all-24-rotations-of-a-3-dimensional-array
def orientations(v: Orientation = (1, 2, 3)) -> Iterator[Orientation]:
    def roll(v):
        return (v[0], v[2], -v[1])

    def turn(v):
        return (-v[1], v[0], v[2])

    for cycle in range(2):
        for step in range(3):  # Yield RTTT 3 times
            v = roll(v)
            yield (v)  #    Yield R
            for i in range(3):  #    Yield TTT
                v = turn(v)
                yield (v)
        v = roll(turn(roll(v)))  # Do RTR


def orient_pts(pts: list[Point], orientation: Orientation) -> list[Point]:
    pts_ort = list()
    for pt in pts:
        signs = [int(copysign(1, o)) for o in orientation]
        axes = [abs(o) - 1 for o in orientation]
        pts_ort.append(tuple([s * pt[a] for s, a in zip(signs, axes)]))
    return pts_ort


def common_points(
    pv0: PointVectors, pv1: PointVectors, min_common_pts=12
) -> tuple[list[Point], list[Point], Vector]:
    """
    Returns 1. common list of points in view of pv0, 2. common list of points in view of pv1
    3. a vector from root point pv0 to pv1
    """
    for p0, vectors0 in pv0.items():
        for p1, vectors1 in pv1.items():
            common_vecs = set(vectors0).intersection(vectors1)
            if len(common_vecs) >= min_common_pts - 1:
                common_pts0 = [p0] + [add(p0, v) for v in common_vecs]
                common_pts1 = [p1] + [add(p1, v) for v in common_vecs]
                return common_pts0, common_pts1, subtract(p0, p1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - Day 19: Beacon Scanner")
    parser.add_argument("-i", help="Input file path")
    args = parser.parse_args()
    file_path = Path(args.i) if args.i else Path("example_input.txt")
    assert file_path.exists()

    views = parse_input_file(file_path)

    pv0 = get_all_point_to_point_vectors(views[0])
    # print(pv0)

    # pv1 = get_all_point_to_point_vectors(views[1])
    # print(pv1)

    # orientations = list(get_all_orientations())
    # print(orientations)

    for orientation in orientations():
        pts1 = orient_pts(views[1], orientation)
        pv1 = get_all_point_to_point_vectors(pts1)
        print("\n", pts1)
        result = common_points(pv0, pv1)
        if result is not None:
            break

    print("YOOOO", result[2])
