from __future__ import annotations

import argparse
import os.path
import re
from dataclasses import dataclass, field

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class Die:
    def __init__(self, sides: int):
        self.sides = sides
        self.side = 0

    def roll3(self) -> int:
        return sum(self.roll() for _ in range(3))

    def roll(self) -> int:
        roll = self.side % self.sides + 1
        self.side += 1
        return roll


@dataclass
class Player:
    id: int
    pos: int
    score: int = field(init=False, default=0)

    @classmethod
    def create(cls, s) -> Player:
        return cls(*(int(c) for c in re.findall(r'\d+', s)))

    def roll(self, die: Die) -> bool:
        self.pos += die.roll3()
        self.score += self.pos % 10 if self.pos % 10 else 10
        return True if self.score >= 1000 else False


def compute(s: str) -> int:
    players = [Player.create(line) for line in s.splitlines()]
    die = Die(100)

    while True:
        for player in players:
            if player.roll(die):
                return players[2 - player.id].score * die.side


INPUT_S = '''\
Player 1 starting position: 4
Player 2 starting position: 8
'''
EXPECTED = 739785


# noinspection DuplicatedCode
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
