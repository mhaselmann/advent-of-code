import argparse
from multiprocessing.sharedctypes import Value
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
                del line_open_chars[-1]
            else:
                return c  # error --> return char with erronous closing symbol
    return line_open_chars  # no errors --> return non-closed opening symbols


def score_erronous_chars(erronous_chars: list[str]) -> int:
    score = 0
    for c in erronous_chars:
        if c == ")":
            score += 3
        elif c == "]":
            score += 57
        elif c == "}":
            score += 1197
        elif c == ">":
            score += 25137
        else:
            raise ValueError(f"{c} can not be scored")
    return score


def score_autocompletion(non_closed_open_chars: list[str]) -> int:
    score = 0
    for c in reversed(non_closed_open_chars):
        score *= 5
        if c == "(":
            score += 1
        elif c == "[":
            score += 2
        elif c == "{":
            score += 3
        elif c == "<":
            score += 4
    return score


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - Day 7: The Treachery of Whales")
    parser.add_argument("-i", help="Input file path")
    args = parser.parse_args()
    path = Path(args.i) if args.i else Path("example_input.txt")
    assert path.exists()

    with open(path) as f:
        erronous_chars = list()
        ac_score = list()
        for line in f:
            residual = resolve_chunks(line)
            if isinstance(residual, str):  # part 1
                erronous_chars.append(residual)
            elif isinstance(residual, list):  # part 2
                ac_score.append(score_autocompletion(residual))

    # Part 1
    error_score = score_erronous_chars(erronous_chars)
    print(f"Answer part 1: Syntax Error Score: {error_score}")

    # Part 2
    ac_score = sorted(ac_score)
    print(f"Answer part 2: Autocompletion Score: {ac_score[int(len(ac_score)/2)]}")
