import argparse
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


class IntersectingRectangles:
    """
    maintain non-overlapping list of rectangles in self.rectangles
    """

    def __init__(self):
        self.rectangles: list[Rectangle] = []

    @staticmethod
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
            return "non-intersect"

    @staticmethod
    def _split(x_: Rectangle, y_: Rectangle) -> list[Rectangle]:
        """
        prerequisite: x_ and y_ must interesect!! check if with _relation
        Returns splitted rectangle along one axis; at maximum one of the splits can still intereset
        with y_ unless split was performed across last dimension.
        Outlook: Splitting is repeated as long as no intersecting
        """
        x_split = []
        for dim, (x, y) in enumerate(zip(x_, y_)):  # iterate through all dimensions
            if x[0] < y[0]:
                x_split.append([*x_[:dim], (x[0], y[0] - 1), *x_[dim + 1 :]])
            if x[1] > y[1]:
                x_split.append([*x_[:dim], (y[1] + 1, x[1]), *x_[dim + 1 :]])
            # append intersecting part
            if len(x_split):
                x_split.append([*x_[:dim], (max(x[0], y[0]), min(x[1], y[1])), *x_[dim + 1 :]])
                print("\n Splitted: ", "x:", x_, "y:", y_, "split:", x_split, "\n")
                return x_split

    def add(self, rectangle: Rectangle):
        """
        Add rectangle ot internal set of non-overlapping rectangles by splitting
        up "input rectangle" into multiple rectangles that do not overlap with
        any other preexisting rectangle.
        """
        new_rectangles = [rectangle]
        for idx, reference in reversed(list(enumerate(self.rectangles))):
            relation = self._relation(rectangle, reference)
            print("\n Relation:", relation, "x:", rectangle, "y:", reference, "\n")
            if relation in ["ident", "enclosed"]:  # no further actions required
                return
            elif relation == "enclosing":  # remove existing rectangle
                del self.rectangles[idx]
            elif relation == "intersect":  # split up
                ad_rectangle = False
                splitted_rectangles = self._split(rectangle, reference)
                for splitted_rectangle in splitted_rectangles:
                    # print("adding splitted rectangle", splitted_rectangle)
                    self.add(splitted_rectangle)
                return
        print("Appending: ", rectangle)
        self.rectangles.append(rectangle)
        print(self.rectangles)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - Day 22: Reactor Reboot")
    parser.add_argument("-i", help="Input file path")
    args = parser.parse_args()
    file_path = Path(args.i) if args.i else Path("example_input.txt")
    assert file_path.exists()

    rectangles = parse_input_file(file_path)
    print(rectangles)

    print(IntersectingRectangles._relation(rectangles[3][0], rectangles[0][0]))

    intersecting_rectangles = IntersectingRectangles()
    intersecting_rectangles.add(rectangles[3][0])
    intersecting_rectangles.add(rectangles[0][0])
    intersecting_rectangles.add(rectangles[1][0])
    intersecting_rectangles.add(rectangles[2][0])
    print(intersecting_rectangles.rectangles)
