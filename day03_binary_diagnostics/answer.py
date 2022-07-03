import argparse
import copy
from pathlib import Path


def bitwise_not_for_fixed_number_of_bits(number, n_bits):
    result = int("1" * n_bits, 2) - number
    assert result >= 0
    return result


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
    epsilon_rate = bitwise_not_for_fixed_number_of_bits(gamma_rate, n_bits)
    return gamma_rate * epsilon_rate


def life_support_rating(path: Path) -> int:
    def get_rating(numbers_str: list[str], filter_most_common: bool) -> int:
        for bit_idx in range(n_bits):  # only consider the first 5 bits
            # filt_bit[0] ... filtered bit in case of more error bits
            filt_bit = ["1", "0"] if filter_most_common else ["0", "1"]
            bit1_bit0 = 0  # sum of one bits minus sum of 0 bits
            for number_str in numbers_str:
                assert number_str[bit_idx] in filt_bit
                bit1_bit0 += 1 if number_str[bit_idx] == "1" else -1
            most_common_bit = filt_bit[0] if bit1_bit0 >= 0 else filt_bit[1]
            numbers_str = [n for n in numbers_str if n[bit_idx] == most_common_bit]
            if len(numbers_str) == 1:
                break
        assert len(numbers_str) == 1
        return int(numbers_str[0], 2)

    with open(path) as f:
        numbers_str = f.readlines()
    n_bits = len(numbers_str[-1])
    o2_gen_rating = get_rating(copy.copy(numbers_str), True)
    co2_gen_rating = get_rating(numbers_str, False)
    return o2_gen_rating * co2_gen_rating


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code Day 03: Binary Diagnostic:")
    parser.add_argument("-i", help="Input file path")
    args = parser.parse_args()
    path = Path(args.i) if args.i else Path("input.txt")
    assert path.exists()

    print(f"Power consumption: {power_consumption(path)}")
    print(f"Live support rating: {life_support_rating(path)}")
