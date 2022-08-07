import argparse
from pathlib import Path


def parse_input_file(file_path: Path) -> tuple[int, int]:
    with open(file_path) as f:
        lines = f.readlines()
    return tuple(int(line.strip().split()[-1]) for line in lines)


def roll_practice_dice_3x(start: int = 1, end: int = 100) -> tuple[int, int]:
    """
    Returns: total number of dice rollings, summed up score of n_rolls
    """
    side = start
    n_dice_rolled = 0
    while True:
        dice_sum = 0
        for _ in range(3):
            dice_sum += side
            side += 1
            n_dice_rolled += 1
            if side > end:
                side = start
        yield n_dice_rolled, dice_sum


def dirac_dice_practice_game(pos1: int, pos2: int) -> tuple[bool, int]:
    """
    Return: bool' variable if player 1 wins, and control score according to puzzle description
    """
    total_score1, total_score2 = 0, 0
    player1_turn = True
    for n_dice_rolled, dice_sum in roll_practice_dice_3x():
        if player1_turn:
            pos1 += dice_sum
            score = pos1 % 10
            total_score1 += score if score > 0 else 10
            if total_score1 >= 1000:
                return True, total_score2 * n_dice_rolled
        else:
            pos2 += dice_sum
            score = pos2 % 10
            total_score2 += score if score > 0 else 10
            if total_score2 >= 1000:
                return False, total_score1 * n_dice_rolled
        player1_turn = not player1_turn


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - Day 21: Dirac Dice")
    parser.add_argument("-i", help="Input file path")
    args = parser.parse_args()
    file_path = Path(args.i) if args.i else Path("example_input.txt")
    assert file_path.exists()

    start_pos = parse_input_file(file_path)
    player1_wins, control_score = dirac_dice_practice_game(*start_pos)
    print(f"Answer part1: {control_score}")
