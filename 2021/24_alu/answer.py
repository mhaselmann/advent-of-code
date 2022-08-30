import argparse
import copy
from pathlib import Path

Variables = dict[str, int]
Program = list[tuple[str, str, str]]


def perform_instruction(variables: Variables, op: str, a: str, b: str | int):
    if isinstance(b, str):
        b = variables[b]
    if op == "add":
        variables[a] += b
    elif op == "mul":
        variables[a] *= b
    elif op == "div":
        variables[a] //= b
    elif op == "mod":
        variables[a] %= b
    elif op == "eql":
        variables[a] = 1 if variables[a] == b else 0


class MONAD:
    def __init__(self, file_path: Path):
        self.variables: Variables = {"w": 0, "x": 0, "y": 0, "z": 0}
        self.programs: list[Program] = []
        self.decreasing_place: list[bool] = []
        self.largest_digits_with_z0: list[int] = []
        with open(file_path) as f:
            for line in f:
                splits = line.split()
                if splits[0] == "inp":
                    self.programs.append([])
                else:
                    op, a = splits[0], splits[1]
                    try:
                        b = int(splits[2])
                    except ValueError:
                        b = splits[2]
                    self.programs[-1].append((op, a, b))
                    if op == "div" and a == "z" and b == 26:
                        self.decreasing_place.append(True)
                    elif op == "div" and a == "z" and b == 1:
                        self.decreasing_place.append(False)
        print(self.decreasing_place)
        assert len(self.programs) == 14 and len(self.decreasing_place) == 14
        self.largest_number_list: list[str, int] = [""] * 14

    def search_largest_number(
        self,
        variables: Variables | None = None,
        place: int = 0,
    ) -> bool:  # part 1
        if variables is None:
            assert place == 0
            variables = {"w": 0, "x": 0, "y": 0, "z": 0}
        else:
            variables = copy.deepcopy(variables)
        program = self.programs[place]
        descreasing = self.decreasing_place[place]
        z_place_before = variables["z"]
        for digit in reversed(range(1, 10)):
            variables_ = copy.deepcopy(variables)
            variables_["w"] = digit
            self.largest_number_list[place] = digit
            for op, a, b in program:
                perform_instruction(variables_, op, a, b)
            print(self.largest_number_list, place, variables_["z"])
            if place == 13 and variables_["z"] == 0:
                # self.largest_number_list[place] = digit
                return True
            elif descreasing and variables_["z"] > z_place_before / 10:
                continue
            else:
                success = self.search_largest_number(variables_, place + 1)
                if success:
                    # self.largest_number_list[place] = digit
                    return True
        self.largest_number_list[place] = ""
        return False  # if all digits are invalid go left

    @property
    def largest_number(self):
        largest_number = map(str, self.largest_number_list)
        largest_number = "".join(largest_number)
        return int(largest_number)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - Day 24: Arithmetic Logic Unit")
    parser.add_argument("-i", help="Input file path")
    args = parser.parse_args()
    file_path = Path(args.i) if args.i else Path("input.txt")
    assert file_path.exists()

    monad = MONAD(file_path)
    monad.search_largest_number()
    print(f"Answer part 1: Larget number with z=0: {monad.largest_number}")
