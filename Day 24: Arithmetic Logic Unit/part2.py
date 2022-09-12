from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def get_relevant_adds(puzzle: list[list[str]]) -> tuple[list[int], list[int]]:
    div1, div26 = [], []
    for i in range(0, len(puzzle), 18):
        if puzzle[i + 4][2] == "1":
            div1.append(int(puzzle[i + 15][2]))
            div26.append(None)
        else:
            div1.append(None)
            div26.append(int(puzzle[i + 5][2]))
    return div1, div26


def get_model_no(div1: list[int], div26: list[int]) -> int:
    modelNo = [0] * 14
    stack = []
    startDigit = 1
    for i, (a, b) in enumerate(zip(div1, div26)):
        if a is not None:
            stack.append((i, a))
        else:
            ia, a = stack.pop()
            diff = a + b
            modelNo[ia] = max(startDigit, startDigit - diff)
            modelNo[i] = max(startDigit, startDigit + diff)
    N = 0
    for n in modelNo:
        N = N * 10 + n
    return N


def compute(s: str) -> int:
    puzzle = [row.split() for row in s.splitlines()]
    div1, div26 = get_relevant_adds(puzzle)
    return get_model_no(div1, div26)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
