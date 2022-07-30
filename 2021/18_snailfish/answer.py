import argparse
import json
from math import ceil
from pathlib import Path
from typing import Annotated, Union, Iterable, Any


SfNumberListRepr = list[Union[int, "SfNumberListRepr"]]  # always 2 elements per list


def get_nested_list_item_by_index_list(l: list, index_list: list) -> Any:
    i = index_list.pop(0)
    return get_nested_list_item_by_index_list(l[i], index_list) if len(index_list) else l[i]


class SfNumber:
    def __init__(self, n: Union["SfNumber", SfNumberListRepr]):
        if isinstance(n, SfNumber):
            self.data = n.data
        elif isinstance(n, list):
            self.data = list()
            self._resolve(n)
        else:
            raise TypeError(f"Input type {type(n)} not supported")

    def _resolve(self, list_repr: SfNumberListRepr, key: int = []):
        if isinstance(list_repr[0], list):
            self._resolve(list_repr[0], key=key + [0])
        else:
            self.data.append((tuple(key + [0]), list_repr[0]))
        if isinstance(list_repr[1], list):
            self._resolve(list_repr[1], key=key + [1])
        else:
            self.data.append((tuple(key + [1]), list_repr[1]))

    def as_list(self) -> SfNumberListRepr:
        list_repr = [None, None]
        for indices, value in self.data:
            i = list(indices)
            if len(i) == 1:
                list_repr[i[0]] = value
            elif len(i) == 2:
                if not isinstance(list_repr[i[0]], list):
                    list_repr[i[0]] = [None, None]
                list_repr[i[0]][i[1]] = value
            elif len(i) == 3:
                if not isinstance(list_repr[i[0]], list):
                    list_repr[i[0]] = [None, None]
                if not isinstance(list_repr[i[0]][i[1]], list):
                    list_repr[i[0]][i[1]] = [None, None]
                list_repr[i[0]][i[1]][i[2]] = value
            elif len(i) == 4:
                if not isinstance(list_repr[i[0]], list):
                    list_repr[i[0]] = [None, None]
                if not isinstance(list_repr[i[0]][i[1]], list):
                    list_repr[i[0]][i[1]] = [None, None]
                if not isinstance(list_repr[i[0]][i[1]][i[2]], list):
                    list_repr[i[0]][i[1]][i[2]] = [None, None]
                list_repr[i[0]][i[1]][i[2]][i[3]] = value
        return list_repr

    def __str__(self):
        return str(f"{self.as_list()}")

    @staticmethod
    def _explode(x: "SfNumber") -> bool:
        for left_idx, (left_loc, _) in enumerate(x.data):
            assert len(left_loc) <= 5
            if len(left_loc) == 5:
                zero_insert_loc = left_loc[:4]
                if left_idx + 2 < len(x.data):
                    x.data[left_idx + 2] = (
                        x.data[left_idx + 2][0],
                        x.data[left_idx + 2][1] + x.data[left_idx + 1][1],
                    )
                del x.data[left_idx + 1]
                if left_idx - 1 >= 0:
                    x.data[left_idx - 1] = (
                        x.data[left_idx - 1][0],
                        x.data[left_idx - 1][1] + x.data[left_idx][1],
                    )
                del x.data[left_idx]
                x.data.insert(left_idx, tuple((tuple(left_loc[:4]), 0)))
                return True
        return False

    @staticmethod
    def _split(x: "SfNumber") -> bool:
        for idx, (loc, value) in enumerate(x.data):
            print(idx, loc, value)
            if value >= 10:
                left_value = int(value / 2)
                left_loc = loc + (0,)
                right_value = ceil(value / 2)
                right_loc = loc + (1,)
                del x.data[idx]
                x.data.insert(idx, (right_loc, right_value))
                x.data.insert(idx, (left_loc, left_value))
                return True
        return False

    @staticmethod
    def reduce(x: "SfNumber") -> "SfNumber":
        while True:
            if SfNumber._explode(x):
                continue
            if SfNumber._split(x):
                continue
            break

    def __add__(self, y: Union["SfNumber", SfNumberListRepr]) -> "SfNumber":
        if isinstance(y, SfNumber):
            y = y.as_list()
        addends = SfNumber([self.as_list(), y])
        SfNumber.reduce(addends)
        return addends


def parse_input_file(file_path: Path) -> list[SfNumberListRepr]:
    with open(file_path) as f:
        lines = f.readlines()
    return [json.loads(line) for line in lines]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - Day 18: Snailfish")
    parser.add_argument("-i", help="Input file path")
    args = parser.parse_args()
    file_path = Path(args.i) if args.i else Path("example_input.txt")
    assert file_path.exists()

    sf_numbers = parse_input_file(file_path)
    # print(sf_numbers, type(sf_numbers[0]))

    sf = SfNumber(sf_numbers[7])

    e = get_nested_list_item_by_index_list(sf_numbers[4], [0, 0, 0, 1])
    print("HERE", e)

    print(sf.data)

    sf.reduce(sf)
    print(sf)
    # print(sf.as_list())

    # print(sf)

    # z = sf + sf

    # print("GOOO  ", z.data)

    # print("ADDED", z.data, sf)
    # print(z)

    # print(sf.as_list())
