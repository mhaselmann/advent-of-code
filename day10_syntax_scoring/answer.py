import argparse
from pathlib import Path


def resolve_chunks(
    line: str, close_open_chars: dict[str, str] = {")": "(", "]": "[", "}": "{", ">": "<"}
) -> list[str] | str:  # empty/non-empty list ... complete/incomplete line, str ... erronous char
    line_open_chars = list()
    for c in line:
        if c in list(close_open_chars.values()):
            line_open_chars.append(c)
        elif c in list(close_open_chars.keys()):
            if close_open_chars[c] == line_open_chars[-1]:
                line_open_chars.pop()
            else:
                return c  # error --> return char with erronous closing symbol
    return line_open_chars  # no errors --> return non-closed opening symbols


def score_erronous_chars(erronous_chars: list[str]) -> int:
    return sum([{")": 3, "]": 57, "}": 1197, ">": 25137}[c] for c in erronous_chars])


def score_autocompletion(non_closed_open_chars: list[str]) -> int:
    score = 0
    for c in reversed(non_closed_open_chars):
        score = (score * 5) + {"(": 1, "[": 2, "{": 3, "<": 4}[c]
    return score


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - Day 7: The Treachery of Whales")
    parser.add_argument("-i", help="Input file path")
    args = parser.parse_args()
    path = Path(args.i) if args.i else Path("example_input.txt")
    assert path.exists()

    with open(path) as f:
        erronous_chars, ac_score = list(), list()
        for line in f:
            residual = resolve_chunks(line)
            if isinstance(residual, str):  # part 1
                erronous_chars.append(residual)
            elif isinstance(residual, list):  # part 2
                ac_score.append(score_autocompletion(residual))

    error_score = score_erronous_chars(erronous_chars)
    print(f"Answer part 1: Syntax Error Score: {error_score}")

    ac_score = sorted(ac_score)
    print(f"Answer part 2: Autocompletion Score: {ac_score[int(len(ac_score)/2)]}")
