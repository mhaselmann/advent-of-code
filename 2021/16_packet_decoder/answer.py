import argparse
from pathlib import Path


def decode_hex_message_to_binary(file_path: Path) -> str:
    with open(file_path) as f:
        message_hex = f.readline()
    groups = list()
    for number_hex in message_hex:
        groups.append(str(bin(int(number_hex, base=16)))[2:].zfill(4))
    return "".join(groups)


def split_binary_msg_into_packages(message: str):
    packages = list()
    bit = 0
    while bit < len(message):
        number_bits = []
        version = int(message[bit : bit + 3], base=2)
        type_id = int(message[bit + 3 : bit + 6], base=2)
        if type_id == 4:
            keep_read = True
            bit += 6
            while keep_read:
                keep_read = True if message[bit] == "1" else False
                number_bits.append(message[bit + 1 : bit + 5])
                bit += 5
            packages.append(
                {
                    "version": version,
                    "type_id": type_id,
                    "number": int("".join(number_bits), base=2),
                }
            )
            package_rest = bit % 4
            if package_rest > 0:
                bit += 4 - bit % 4
        else:
            length_type_id = message[bit + 6]
            bit += 6
            if length_type_id == "0":
                subpackage_length = int(message[bit : bit + 15], 2)
                bit += 15

        print(packages)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - Day 16: Packet Decoder")
    parser.add_argument("-i", help="Input file path")
    args = parser.parse_args()
    file_path = Path(args.i) if args.i else Path("example_input.txt")
    assert file_path.exists()

    message = decode_hex_message_to_binary(file_path)
    print(message)
    split_binary_msg_into_packages(message)
