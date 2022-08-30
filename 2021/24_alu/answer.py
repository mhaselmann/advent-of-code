import argparse
import copy
from pathlib import Path

Variables = dict[str, int]
Program = list[tuple[str, str, str]]


def digit_list_as_int(digit_list: list[str | int]):
    number = map(str, digit_list)
    number = "".join(number)
    try:
        return int(number)
    except ValueError:
        return None


def perform_instruction(vars_: Variables, op: str, a: str, b: str | int):
    if isinstance(b, str):
        b = vars_[b]
    if op == "add":
        vars_[a] += b
    elif op == "mul":
        vars_[a] *= b
    elif op == "div":
        vars_[a] //= b
    elif op == "mod":
        vars_[a] %= b
    elif op == "eql":
        vars_[a] = 1 if vars_[a] == b else 0


class Monad:
    def __init__(self, file_path: Path):
        self.programs: list[Program] = []
        self.descrease: list[bool] = []
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
                        self.descrease.append(True)
                    elif op == "div" and a == "z" and b == 1:
                        self.descrease.append(False)
        assert len(self.programs) == 14 and len(self.descrease) == 14
        self.digit_list: list[str | int] = [""] * 14

    def _search_number(
        self,
        largest: bool,
        parent_vars: Variables = {"w": 0, "x": 0, "y": 0, "z": 0},
        place: int = 0,
    ) -> bool:
        """
        * blocks with div z 1 -> always increases
        * blocks diz z 26 -> force a decrease by factor of approx. 1/26
        """
        digit_seq = reversed(range(1, 10)) if largest else range(1, 10)
        for digit in digit_seq:
            vars_ = copy.deepcopy(parent_vars)
            vars_["w"] = digit
            self.digit_list[place] = digit
            for op, a, b in self.programs[place]:
                perform_instruction(vars_, op, a, b)
            if place == 13 and vars_["z"] == 0:
                return True
            elif self.descrease[place] and vars_["z"] > parent_vars["z"] / 10:
                continue
            elif self._search_number(largest, vars_, place + 1):
                return True
        self.digit_list[place] = ""
        return False  # if all digits are invalid go left

    def search_largest_number(self):
        self.digit_list: list[str, int] = [""] * 14
        self._search_number(largest=True)
        return digit_list_as_int(self.digit_list)

    def search_smallest_number(self):
        self.digit_list: list[str, int] = [""] * 14
        self._search_number(largest=False)
        return digit_list_as_int(self.digit_list)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - Day 24: Arithmetic Logic Unit")
    parser.add_argument("-i", help="Input file path")
    args = parser.parse_args()
    file_path = Path(args.i) if args.i else Path("input.txt")
    assert file_path.exists()

    monad = Monad(file_path)
    print(f"Answer part 1 - Larget number with z=0: {monad.search_largest_number()}")
    print(f"Answer part 2 - Smallest number with z=0: {monad.search_smallest_number()}")
