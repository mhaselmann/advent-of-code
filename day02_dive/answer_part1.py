import argparse
from pathlib import Path


def final_depth_and_hor_pos(path: Path) -> tuple[int, int]:
    depth = 0
    hor_pos = 0
    with open(path) as f:
        for line in f:
            direction, units = line.split(" ")
            if direction == "forward":
                hor_pos += int(units)
            elif direction == "up":
                depth -= int(units)
            elif direction == "down":
                depth += int(units)
            else:
                raise ValueError(f"Command {direction} not implemented")
    return depth, hor_pos


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Final position of submarin going forward, down and up by certain units:"
    )
    parser.add_argument("-i", help="Input file path")
    args = parser.parse_args()
    path = Path(args.i) if args.i else Path("example_input.txt")
    assert path.exists()

    depth, hor_pos = final_depth_and_hor_pos(path)
    print(f"Depth: {depth}, Hor. Pos.: {hor_pos}, Answer: {depth * hor_pos}")
