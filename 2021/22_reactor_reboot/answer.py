import argparse
import copy
from math import prod
import re
from pathlib import Path

# Rectangles of any dimension: 3-dim -> Cube
# bool indicating wheter add (on) or subtract (off)
Rectangle = list[tuple[int, int]]


def parse_input_file(file_path: Path) -> list[tuple[bool, Rectangle]]:
    """
    Returns a list of tuples containing an any-dimensional rectangle
    (Cubes in this example) with a bool variable indicating wheter the rectangle
    has to be added or subtracted from a set of rectangles
    """
    rectangles: list[Rectangle] = []
    with open(file_path) as f:
        for line in f:
            line_parts = re.split(",| ", line)
            add_rectangle = True if line_parts[0] == "on" else False
            rectangle = []
            for dim_str in line_parts[1:]:
                p = dim_str.split("..")
                rectangle.append((int(p[0].split("=")[1]), int(p[1])))
            rectangles.append((rectangle, add_rectangle))
    return rectangles


def _relation(x_: Rectangle, y_: Rectangle) -> str:
    x_enclosing_y = True
    x_enclosed_in_y = True
    intersecting = True
    for x, y in zip(x_, y_):
        # enclosing
        if not (x[0] <= y[0] and x[1] >= y[1]):
            x_enclosing_y = False
        # enclosed
        if not (x[0] >= y[0] and x[1] <= y[1]):
            x_enclosed_in_y = False
        # intersecting
        if not (x[0] >= y[0] and x[0] <= y[1] or x[1] >= y[0] and x[1] <= y[1]):
            intersecting = False
    if x_enclosing_y and x_enclosed_in_y:
        return "ident"
    elif x_enclosing_y:
        return "enclosing"
    elif x_enclosed_in_y:
        return "enclosed"
    elif intersecting:
        return "intersect"
    else:
        return "no_intersect"


def _split(x_: Rectangle, z_: Rectangle) -> list[Rectangle]:
    """
    prerequisite: x_ and z_ must interesect!! check if with _relation
    Returns splitted rectangle along one axis; at maximum one of the splits can still intereset
    with z_ unless split was performed across last dimension.
    Outlook: Splitting is repeated as long as no intersecting
    """
    x_split = []
    for dim, (x, z) in enumerate(zip(x_, z_)):  # iterate through all dimensions
        if x[0] < z[0]:
            x_split.append([*x_[:dim], (x[0], z[0] - 1), *x_[dim + 1 :]])
        if x[1] > z[1]:
            x_split.append([*x_[:dim], (z[1] + 1, x[1]), *x_[dim + 1 :]])
        # append intersecting part
        if len(x_split):
            x_split.append([*x_[:dim], (max(x[0], z[0]), min(x[1], z[1])), *x_[dim + 1 :]])
            # print("\n Splitted: ", "x:", x_, "z:", z_, "split:", x_split, "\n")
            return x_split


def _subtract(z_: Rectangle, x_: Rectangle, res: list[Rectangle]):
    """
    Subtract intersecting or enclosed rectangle x from rectangle z set by splitting
    z in multiple rectangles that do not overlap with x; delete self.rectangles
    that are enclosed in rectangle
    """
    relation = _relation(z_, x_)
    if relation == "no_intersect":
        res.append(z_)
    elif relation in ["enclosing", "intersect"]:
        # print(relation, "_____________splitting: ", z_, x_)
        splits = _split(z_, x_)
        for s in splits:
            _subtract(s, x_, res)


class IntersectingRectangles:
    """
    maintain non-overlapping list of rectangles in self.rectangles
    """

    def __init__(self):
        self.rectangles: list[Rectangle] = []

    def add(self, x: Rectangle):
        """
        Add rectangle ot internal set of non-overlapping rectangles by splitting
        up "input rectangle" into multiple rectangles that do not overlap with
        any other preexisting rectangle.
        """
        for idx, rect in reversed(list(enumerate(self.rectangles))):
            relation = _relation(x, rect)
            # print("\n Relation:", relation, "x:", x, "y:", rect, "\n")
            if relation in ["ident", "enclosed"]:  # no further actions required
                return
            elif relation == "enclosing":  # remove existing rectangle
                del self.rectangles[idx]
            elif relation == "intersect":  # split up
                splitted_rectangles = _split(x, rect)
                for splitted_rectangle in splitted_rectangles:
                    self.add(splitted_rectangle)
                return
        # print("Appending: ", x)
        self.rectangles.append(x)

    def subtract(self, x: Rectangle):
        """
        Subtract rectangle from self.rectangles set by splitting self.rectangles in rectangles
        that do not overlap with rectangle; delete self.rectangles that are enclosed in rectangle
        """
        new_rectangles = []
        for r in self.rectangles:
            _subtract(r, x, new_rectangles)
        self.rectangles = new_rectangles

    def sum(self):
        sum = 0
        for r_ in self.rectangles:
            side_lengths = []
            for r in r_:
                side_lengths.append(r[1] - r[0] + 1)
            sum += prod(side_lengths)
        return sum


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - Day 22: Reactor Reboot")
    parser.add_argument("-i", help="Input file path")
    args = parser.parse_args()
    file_path = Path(args.i) if args.i else Path("example_input.txt")
    assert file_path.exists()

    rectangles = parse_input_file(file_path)
    intersecting_rectangles = IntersectingRectangles()
    for r_, add in rectangles:
        consider = True
        for r in r_:
            if abs(r[0] > 50) or abs(r[1] > 50):
                consider = False
        if consider:
            if add:
                intersecting_rectangles.add(r_)
            else:
                intersecting_rectangles.subtract(r_)
        print(r_, intersecting_rectangles.sum())
    print(intersecting_rectangles.sum())
