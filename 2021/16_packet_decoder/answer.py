import argparse
from pathlib import Path
from typing import Optional


VERSION_SUM = 0


def decode_hex_message_to_binary(file_path: Path) -> str:
    with open(file_path) as f:
        message_hex = f.readline()
    groups = list()
    for number_hex in message_hex:
        groups.append(str(bin(int(number_hex, base=16)))[2:].zfill(4))
    return "".join(groups)


def split_binary_msg_into_packages(msg: str, bit: int = 0, n_subpackages: Optional[int] = None):
    global VERSION_SUM
    packages = []
    while bit + 8 < len(msg):
        version = int(msg[bit : bit + 3], base=2)
        type_id = int(msg[bit + 3 : bit + 6], base=2)
        VERSION_SUM += version
        packages.append(
            {
                "version": version,
                "type_id": type_id,
            }
        )
        if packages[-1]["type_id"] == 4:
            literal_value_bits = []
            keep_read = True
            bit += 6
            while keep_read:
                keep_read = True if msg[bit] == "1" else False
                literal_value_bits.append(msg[bit + 1 : bit + 5])
                bit += 5
                packages[-1]["number"] = int("".join(literal_value_bits), base=2)
        else:
            packages[-1]["type_length_id"] = msg[bit + 6]
            bit += 7
            if packages[-1]["type_length_id"] == "0":
                packages[-1]["subpackage_length"] = int(msg[bit : bit + 15], 2)
                bit += 15
                packages[-1]["subpackages"], bit = split_binary_msg_into_packages(msg, bit)
            else:
                packages[-1]["n_subpackages"] = int(msg[bit : bit + 11], 2)
                bit += 11
                packages[-1]["subpackages"], bit = split_binary_msg_into_packages(
                    msg, bit, packages[-1]["n_subpackages"]
                )
        if n_subpackages:
            n_subpackages += 1
            if len(packages) >= n_subpackages:
                return packages, bit
    return packages, bit


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - Day 16: Packet Decoder")
    parser.add_argument("-i", help="Input file path")
    args = parser.parse_args()
    file_path = Path(args.i) if args.i else Path("example_input.txt")
    assert file_path.exists()

    message = decode_hex_message_to_binary(file_path)
    print(message)
    packages, bit = split_binary_msg_into_packages(message, 0)
    print("\n\n\n", packages, VERSION_SUM)
