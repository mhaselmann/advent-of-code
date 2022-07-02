import argparse
from pathlib import Path


def bitwise_not_fixed_n_bits(number, n_bits):
    return int("1" * n_bits, 2) - number


def power_consumption(path: Path) -> int:
    # read lines, determine number of bits per line, initialize
    with open(path) as f:
        numbers_str = f.readlines()
    n_bits = len(numbers_str[-1])
    gamma_rate_str = ""

    # iterate though each bit position over all lines and compare 1,0-sums
    for bit_idx in range(n_bits):
        bit1_bit0 = 0  # sum of one bits minus sum of 0 bits
        for number_str in numbers_str:
            assert number_str[bit_idx] in ["0", "1"]
            bit1_bit0 += 1 if number_str[bit_idx] == "1" else -1
        assert bit1_bit0 != 0
        gamma_rate_str += "1" if bit1_bit0 > 0 else "0"

    # compute epsilon rate and power consumption
    gamma_rate = int(gamma_rate_str, 2)
    epsilon_rate = bitwise_not_fixed_n_bits(gamma_rate, n_bits)
    return gamma_rate * epsilon_rate


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code Day 03: Binary Diagnostic:")
    parser.add_argument("-i", help="Input file path")
    args = parser.parse_args()
    path = Path(args.i) if args.i else Path("input.txt")
    assert path.exists()

    print(f"Power consumption: {power_consumption(path)}")
