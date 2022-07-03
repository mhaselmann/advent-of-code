import argparse
import copy
from pathlib import Path
from typing import Optional

import numpy as np


class Board:
    def __init__(self, board: list[list[int]]):
        self._board = np.array(board)
        assert self._board.shape == (5, 5)
        self._marked = np.zeros(self._board.shape, dtype=bool)
        self._last_called_number: Optional[int] = None

    def mark(self, number: int):
        self._last_called_number = number
        self._marked[self._board == number] = True

    def is_win(self) -> bool:
        # check horizontal and vertical lines
        for idx in range(5):
            if np.sum(self._marked[:, idx]) == 5 or np.sum(self._marked[idx, :]) == 5:
                return True
        # check diagonals  (they don't count, lol)
        # if np.sum(np.diag(self._marked)) == 5 or np.sum(np.diag(np.fliplr(self._marked))) == 5:
        #     return True
        return False

    def final_score(self) -> int:
        return np.sum(self._board[~self._marked]) * self._last_called_number

    def __str__(self):
        return f"\n{self.__class__}\n{self._board}\n{self._marked}\n{self._last_called_number}\n"


def parse_input(path: Path) -> tuple[list[Board], list[int]]:
    boards: list[Board] = []
    current_board: list[list[int]] = []
    with open(path) as f:
        for line_idx, line in enumerate(f):
            if line_idx == 0:  # read out bingo sequence from first line
                seq = [int(n) for n in line.split(",")]
                continue
            if line[0] == "\n":  # skip empty lines
                if len(current_board) == 0:
                    continue
                boards.append(Board(current_board))
                current_board = []
                continue
            current_board.append([int(n) for n in line.split()])
        # add last boards if no empty line is at end of document
        if len(current_board) == 5:
            boards.append(Board(current_board))
    return boards, seq


# why is it so slow?
def get_first_winning_board(boards: list[Board], seq: list[int]) -> Board:
    for number in seq:
        for board in boards:
            board.mark(number)
            if board.is_win():
                return board
    raise ValueError(f"Sequence {seq} not long enough for any board to win")


def get_last_winning_board(boards: list[Board], seq: list[int]) -> Board:
    boards.reverse()
    for number in seq:
        for idx in reversed(range(len(boards))):
            boards[idx].mark(number)
            if boards[idx].is_win():
                if len(boards) == 1:
                    return boards[idx]
                else:
                    del boards[idx]
    raise ValueError(f"Sequence {seq} not long enough for all boards to win")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code Day 03: Binary Diagnostic:")
    parser.add_argument("-i", help="Input file path")
    args = parser.parse_args()
    path = Path(args.i) if args.i else Path("input.txt")
    assert path.exists()
    boards, seq = parse_input(path)

    winner_board = get_first_winning_board(copy.deepcopy(boards), seq)
    print(f"First winning board: {winner_board} with final score {winner_board.final_score()}")

    worst_board = get_last_winning_board(boards, seq)
    print(f"\n \n Last winning board: {worst_board} with final score {worst_board.final_score()}")
