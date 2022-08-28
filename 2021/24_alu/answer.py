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

    def search_largest_number_with_z0(self):
        for digit_place, program in enumerate(self.programs):
            for digit in reversed(range(1, 10)):  # 9, 8, ..., 2, 1
                variables = copy.deepcopy(self.variables)
                variables["w"] = digit
                for op, a, b in program:
                    # print("before", variables, op, a, b)
                    perform_instruction(variables, op, a, b)
                    # print("after", variables)
                print(digit_place, digit, variables)
                if variables["z"] == 0:
                    print(f"Largest digit at place {digit_place}: {digit}")
                    self.variables = variables
                    break
            self.variables = variables


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - Day 24: Arithmetic Logic Unit")
    parser.add_argument("-i", help="Input file path")
    args = parser.parse_args()
    file_path = Path(args.i) if args.i else Path("input.txt")
    assert file_path.exists()

    monad = MONAD(file_path)
    print(monad.programs[0])
    monad.search_largest_number_with_z0()
