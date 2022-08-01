import argparse
import copy
import itertools
from math import copysign
from pathlib import Path
from typing import Generator, Optional


Point, Vector = tuple[int, ...], tuple[int, ...]
Signs, Axes = tuple[int, int, int], tuple[int, int, int]
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
def orientations() -> Generator[tuple[Signs, Axes], None, None]:
    v = (1, 2, 3)
    roll = lambda v: (v[0], v[2], -v[1])
    turn = lambda v: (-v[1], v[0], v[2])
    signs = lambda v: [int(copysign(1, o)) for o in v]
    axes = lambda v: [abs(o) - 1 for o in v]
    for _ in range(2):
        for _ in range(3):  # Yield RTTT 3 times
            v = roll(v)
            yield (signs(v), axes(v))  #    Yield R
            for _ in range(3):  #    Yield TTT
                v = turn(v)
                yield (signs(v), axes(v))
        v = roll(turn(roll(v)))  # Do RTR


def orient_pts(pts: list[Point], signs: Signs, axes: Axes) -> list[Point]:
    pts_ort = list()
    for pt in pts:
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


def try_register_view(view_pts: list[Point], root_view_pv: PointVectors) -> Optional[list[Point]]:
    """
    Tries to register view by comparing all of its 24 orientations with registered view.
    if at least 12 points (11 vectors) match return registered view of first argument
    and a list of the common points. If the points do not match in any orientation return None
    """
    for signs, axes in orientations():
        view_pts_out = orient_pts(view_pts, signs, axes)
        pv = get_all_point_to_point_vectors(view_pts_out)
        result = common_points(root_view_pv, pv)
        if result is not None:
            _, _, delta = result
            view_pts_out = [add(pt, delta) for pt in view_pts_out]
            return view_pts_out


def register_all_views(views: Views, root_view: Views) -> Views:
    assert len(root_view) == 1
    root_view_key = list(root_view.keys())[0]
    reg_views = copy.deepcopy(root_view)
    unused_reg_view_keys = list(root_view.keys())
    reg_views_pv = {root_view_key: get_all_point_to_point_vectors(root_view[root_view_key])}
    while len(unused_reg_view_keys):
        new_unused_reg_view_keys = list()
        for view_key, view_pts in views.items():
            for reg_view_key in unused_reg_view_keys:
                new_reg_view_pts = try_register_view(
                    view_pts=view_pts, root_view_pv=reg_views_pv[reg_view_key]
                )
                if new_reg_view_pts is not None:
                    reg_views[view_key] = new_reg_view_pts
                    reg_views_pv[view_key] = get_all_point_to_point_vectors(new_reg_view_pts)
                    new_unused_reg_view_keys.append(view_key)
                    break

        # delete new_unused_reg_view_keys from views
        for view_key in new_unused_reg_view_keys:
            del views[view_key]
        unused_reg_view_keys = new_unused_reg_view_keys.copy()
    return reg_views


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - Day 19: Beacon Scanner")
    parser.add_argument("-i", help="Input file path")
    args = parser.parse_args()
    file_path = Path(args.i) if args.i else Path("example_input.txt")
    assert file_path.exists()

    views = parse_input_file(file_path)
    root_view = {0: views[0]}
    del views[0]
    reg_views = register_all_views(views, root_view)
    all_pts = set(itertools.chain(*list(reg_views.values())))
    print(f"Answer part 1: How many beacons are there: {len(all_pts)}")
