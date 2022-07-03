import argparse
from pathlib import Path
from typing import Optional

import numpy as np


class BingoBoard:
    def __init__(self, board: list[list[int]]):
        self.board = np.array(board)
        assert self.board.shape == (5, 5)
        self.marked = np.zeros(self.board.shape, dtype=bool)
        self.last_called_number: Optional[int] = None

    def mark(self, number: int):
        self.last_called_number = number
        self.marked[self.board == number] = True

    def is_win(self) -> bool:
        # check horizontal and vertical lines
        for idx in range(5):
            if np.sum(self.marked[:, idx]) == 5 or np.sum(self.marked[idx, :]) == 5:
                return True
        # check diagonals  (they don't count, lol)
        # if np.sum(np.diag(self.marked)) == 5 or np.sum(np.diag(np.fliplr(self.marked))) == 5:
        #     return True
        return False

    def final_score(self) -> int:
        return np.sum(self.board[~self.marked]) * self.last_called_number


def parse_input(path: Path) -> tuple[list[BingoBoard], list[int]]:
    boards: list[BingoBoard] = []
    current_board: list[list[int]] = []
    with open(path) as f:
        for line_idx, line in enumerate(f):
            if line_idx == 0:  # read out bingo sequence from first line
                seq = [int(n) for n in line.split(",")]
                continue
            if line[0] == "\n":  # skip empty lines
                if len(current_board) == 0:
                    continue
                boards.append(BingoBoard(current_board))
                current_board = []
                continue
            current_board.append([int(n) for n in line.split()])
        # add last boards if no empty line is at end of document
        if len(current_board) == 5:
            boards.append(BingoBoard(current_board))
    return boards, seq


# why is it so slow?
def get_first_winning_board(
    boards: list[BingoBoard], seq: list[int]
) -> BingoBoard:  # also return last called number of seq
    for number in seq:
        for board in boards:
            board.mark(number)
            if board.is_win():
                return board
    raise ValueError(f"Sequence {seq} not long enough for any board to win")


if __name__ == "__main__":
    import time

    parser = argparse.ArgumentParser(description="Advent of Code Day 03: Binary Diagnostic:")
    parser.add_argument("-i", help="Input file path")
    args = parser.parse_args()
    path = Path(args.i) if args.i else Path("input.txt")
    assert path.exists()

    t0 = time.time()
    boards, seq = parse_input(path)
    winner_board = get_first_winning_board(boards=boards, seq=seq)
    t_delta = time.time() - t0
    print(f"First winning board ({t_delta}s): \n {winner_board.board} \n {winner_board.marked}")
    print(f"Final score: {winner_board.final_score()}")
