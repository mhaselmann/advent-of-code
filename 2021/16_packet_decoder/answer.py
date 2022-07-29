import argparse
from math import prod
from pathlib import Path
from typing import Optional


Packet = dict[str, int | list["Packet"]]

SUM, PROD, MIN, MAX, LITERAL, GT, LT, EQ = range(8)
OPS = {
    SUM: sum,
    PROD: prod,
    MIN: min,
    MAX: max,
    GT: lambda x: 1 if x[0] > x[1] else 0,
    LT: lambda x: 1 if x[0] < x[1] else 0,
    EQ: lambda x: 1 if x[0] == x[1] else 0,
}


def get_binary_msg_from_file(file_path: Path) -> str:
    with open(file_path) as f:
        msg_hex = f.readline()
    return "".join([str(bin(int(n, base=16)))[2:].zfill(4) for n in msg_hex])


def decode_binary_msg(
    msg: str,
    _bit: int = 0,
    _n_sps: Optional[int] = None,
    _sps_len: Optional[int] = None,
) -> list[Packet]:
    """
    Parse packets from binary message "msg" and returns list of packets
    """
    packets = []
    start_bit = _bit
    while _bit + 8 < len(msg):
        packets.append(
            {
                "version": int(msg[_bit : _bit + 3], base=2),
                "type_id": int(msg[_bit + 3 : _bit + 6], base=2),
            }
        )
        if packets[-1]["type_id"] == LITERAL:  # literal value package
            literal_value_bits = []
            keep_read = True
            _bit += 6
            while keep_read:
                keep_read = True if msg[_bit] == "1" else False
                literal_value_bits.append(msg[_bit + 1 : _bit + 5])
                _bit += 5
                packets[-1]["number"] = int("".join(literal_value_bits), base=2)
        else:  # operator package
            packets[-1]["type_len_id"] = msg[_bit + 6]
            _bit += 7
            if packets[-1]["type_len_id"] == "0":  # fixed length sps
                packets[-1]["sps_len"] = int(msg[_bit : _bit + 15], 2)
                _bit += 15
                packets[-1]["sps"], _bit = decode_binary_msg(
                    msg, _bit, _sps_len=packets[-1]["sps_len"]
                )
            else:  # fixed number of sps
                packets[-1]["n_sps"] = int(msg[_bit : _bit + 11], 2)
                _bit += 11
                packets[-1]["sps"], _bit = decode_binary_msg(
                    msg, _bit, _n_sps=packets[-1]["n_sps"]
                )
        # check return conditions in case of sps
        if _n_sps and len(packets) >= _n_sps:  # parent type_id == 1
            return packets, _bit
        elif _sps_len and _bit >= start_bit + _sps_len:  # parent type_id == 0
            return packets, _bit
    return packets


def version_sum(packets: list[Packet], _counter=0) -> int:
    for packet in packets:
        _counter += packet["version"]
        if "sps" in packet:
            _counter += version_sum(packet["sps"])
    return _counter


def calc_packet_expr(packets: list[Packet]) -> list[int]:
    res = []
    for packet in packets:
        if packet["type_id"] == LITERAL:  # literal value packet
            res.append(packet["number"])
        else:  # operator packets
            sps_res = calc_packet_expr(packet["sps"])
            res.append(OPS[packet["type_id"]](sps_res))
    return res


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - Day 16: Packet Decoder")
    parser.add_argument("-i", help="Input file path")
    args = parser.parse_args()
    file_path = Path(args.i) if args.i else Path("example_input.txt")
    assert file_path.exists()

    message = get_binary_msg_from_file(file_path)
    packets = decode_binary_msg(message)
    print(f"Answer part 1: Version sum: {version_sum(packets)}")
    print(f"Answer part 2: Expression result: {calc_packet_expr(packets)[0]}")
