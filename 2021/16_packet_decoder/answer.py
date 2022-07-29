import argparse
import functools
import operator
from pathlib import Path
from typing import Optional


Package = dict[str, int | list["Package"]]


def decode_binary_message_from_file(file_path: Path) -> str:
    with open(file_path) as f:
        message_hex = f.readline()
    groups = list()
    for number_hex in message_hex:
        groups.append(str(bin(int(number_hex, base=16)))[2:].zfill(4))
    return "".join(groups)


def parse_packages(
    msg: str,
    _bit: int = 0,
    _n_subpackages: Optional[int] = None,
    _subpackage_length: Optional[int] = None,
) -> list[Package]:
    """
    Parse packages from binary message "msg" and returns list of packages
    """
    packages = []
    start_bit = _bit
    while _bit + 8 < len(msg):
        packages.append(
            {
                "version": int(msg[_bit : _bit + 3], base=2),
                "type_id": int(msg[_bit + 3 : _bit + 6], base=2),
            }
        )
        if packages[-1]["type_id"] == 4:  # literal value package
            literal_value_bits = []
            keep_read = True
            _bit += 6
            while keep_read:
                keep_read = True if msg[_bit] == "1" else False
                literal_value_bits.append(msg[_bit + 1 : _bit + 5])
                _bit += 5
                packages[-1]["number"] = int("".join(literal_value_bits), base=2)
        else:  # operator package
            packages[-1]["type_length_id"] = msg[_bit + 6]
            _bit += 7
            if packages[-1]["type_length_id"] == "0":  # fixed length subpackages
                packages[-1]["subpackage_length"] = int(msg[_bit : _bit + 15], 2)
                _bit += 15
                packages[-1]["subpackages"], _bit = parse_packages(
                    msg, _bit, _subpackage_length=packages[-1]["subpackage_length"]
                )
            else:  # fixed number of subpackages
                packages[-1]["n_subpackages"] = int(msg[_bit : _bit + 11], 2)
                _bit += 11
                packages[-1]["subpackages"], _bit = parse_packages(
                    msg, _bit, _n_subpackages=packages[-1]["n_subpackages"]
                )
        # check return conditions in case of subpackages
        if _n_subpackages and len(packages) >= _n_subpackages:  # parent type_id == 1
            return packages, _bit
        elif _subpackage_length and _bit >= start_bit + _subpackage_length:  # parent type_id == 0
            return packages, _bit
    return packages


def version_sum(packages: list[Package], _counter=0) -> int:
    for package in packages:
        _counter += package["version"]
        if "subpackages" in package:
            _counter += version_sum(package["subpackages"])
    return _counter


def calculate_expressions(packages: list[Package]) -> list[int]:
    results = []
    for package in packages:
        if package["type_id"] == 4:  # literal value package
            results.append(package["number"])
        else:  # operator packages
            subpackages_results = calculate_expressions(package["subpackages"])
            if package["type_id"] == 0:  # sum operator
                results.append(sum(subpackages_results))
            elif package["type_id"] == 1:  # product operator
                results.append(functools.reduce(operator.mul, subpackages_results))
            elif package["type_id"] == 2:  # min operator
                results.append(min(subpackages_results))
            elif package["type_id"] == 3:  # max operator
                results.append(max(subpackages_results))
            elif package["type_id"] == 5:  # greater than
                assert len(subpackages_results) == 2, f"{package} >"
                results.append(1 if subpackages_results[0] > subpackages_results[1] else 0)
            elif package["type_id"] == 6:  # less than
                assert len(subpackages_results) == 2, f"{package} <"
                results.append(1 if subpackages_results[0] < subpackages_results[1] else 0)
            elif package["type_id"] == 7:  # equal to
                assert len(subpackages_results) == 2, f"{package} =="
                results.append(1 if subpackages_results[0] == subpackages_results[1] else 0)
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - Day 16: Packet Decoder")
    parser.add_argument("-i", help="Input file path")
    args = parser.parse_args()
    file_path = Path(args.i) if args.i else Path("example_input.txt")
    assert file_path.exists()

    message = decode_binary_message_from_file(file_path)
    packages = parse_packages(message)
    print(f"Answer part 1: Sum of all package/subpackage versions: {version_sum(packages)}")
    print(f"Answer part 2: Expression's result: {calculate_expressions(packages)[0]}")
