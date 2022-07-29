import argparse
import functools
import operator
from pathlib import Path
from typing import Optional, Union


Package = dict[str, Union[int, list["Package"]]]


def decode_binary_message_from_file(file_path: Path) -> str:
    with open(file_path) as f:
        message_hex = f.readline()
    groups = list()
    for number_hex in message_hex:
        groups.append(str(bin(int(number_hex, base=16)))[2:].zfill(4))
    return "".join(groups)


def parse_packages(msg: str, bit: int = 0, n_subpackages: Optional[int] = None) -> list[Package]:
    """
    Parse packages from binary message "msg" and returns list of packages
    """
    packages = []
    while bit + 8 < len(msg):
        packages.append(
            {
                "version": int(msg[bit : bit + 3], base=2),
                "type_id": int(msg[bit + 3 : bit + 6], base=2),
            }
        )
        if packages[-1]["type_id"] == 4:  # literal value package
            literal_value_bits = []
            keep_read = True
            bit += 6
            while keep_read:
                keep_read = True if msg[bit] == "1" else False
                literal_value_bits.append(msg[bit + 1 : bit + 5])
                bit += 5
                packages[-1]["number"] = int("".join(literal_value_bits), base=2)
        else:  # operator package
            packages[-1]["type_length_id"] = msg[bit + 6]
            bit += 7
            if packages[-1]["type_length_id"] == "0":  # fixed length subpackages
                packages[-1]["subpackage_length"] = int(msg[bit : bit + 15], 2)
                bit += 15
                packages[-1]["subpackages"], bit = parse_packages(msg, bit)
                print("\n \n HERE111111: ", packages[-1]["subpackages"])
            else:  # fixed number of subpackages
                packages[-1]["n_subpackages"] = int(msg[bit : bit + 11], 2)
                bit += 11
                packages[-1]["subpackages"], bit = parse_packages(
                    msg, bit, packages[-1]["n_subpackages"]
                )
                print("\n \n HERE222222: ", packages[-1]["subpackages"])
        if n_subpackages:  # in case parent is operator package with fixed number of subpackages
            n_subpackages += 1
            if len(packages) >= n_subpackages:
                return packages, bit
    return packages, bit


def version_sum(packages: list[Package], counter=0) -> int:
    for package in packages:
        counter += package["version"]
        if "subpackages" in package:
            counter += version_sum(package["subpackages"])
    return counter


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
    packages, _ = parse_packages(message)
    print(f"Answer part 1: Sum of all package/subpackage versions: {version_sum(packages)}")

    print(packages)

    print(calculate_expressions(packages))
