from dataclasses import dataclass
from typing import List, Tuple

import numpy as np

with open("numbers.txt") as f:
    number_str = f.readline().split(",")
    rolls = [int(n) for n in number_str]


@dataclass
class Board:
    field: np.ndarray
    marked: List[Tuple[int]]

    def mark(self, roll) -> None:
        result = np.where(self.field == roll)
        listOfCoordinates = list(zip(result[0], result[1]))
        for coordinate in listOfCoordinates:
            self.marked.append(coordinate)

    def calc_score(self, roll) -> int:
        for coord in self.marked:
            self.field[coord] = 0
        return self.field.sum() * roll

    def check_win(self) -> bool:
        x_coords = []
        y_coords = []
        for coord in self.marked:
            x_coords.append(coord[0])
            y_coords.append(coord[1])
        for i in range(0, 4):
            if x_coords.count(i) == 5 or y_coords.count(i) == 5:
                return True
        return False


def create_boards() -> list[Board]:
    boards = []
    board_str = open("boards.txt").read().split("\n\n")
    for board in board_str:
        rows = board.split("\n")
        board_lst = []
        for row in rows:
            numbers_str = row.split(" ")
            for i, number in enumerate(numbers_str):
                if number == '':
                    del numbers_str[i]
            numbers = [int(n) for n in numbers_str]
            board_lst.append(numbers)
        board = np.array(board_lst)
        boards.append(Board(board, []))
    return boards


def main():
    boards = create_boards()
    for roll in rolls:
        for board in boards:
            board.mark(roll)
            if board.check_win():
                score = board.calc_score(roll)
                return score


if __name__ == '__main__':
    print(main())
