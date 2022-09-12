from __future__ import annotations

import argparse
import collections
import os.path
import re
from dataclasses import dataclass, field

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

die_rolls = collections.Counter(i + j + k for i in (1, 2, 3) for j in (1, 2, 3) for k in (1, 2, 3))


@dataclass
class Player:
    id: int
    pos: int
    score: int = field(default=0)

    @classmethod
    def create(cls, s) -> Player:
        return cls(*(int(c) for c in re.findall(r'\d+', s)))

    def roll(self) -> tuple[list[tuple[Player, int]], int]:
        new_players = []
        wins = 0
        for roll, ct in die_rolls.items():
            pos = (self.pos + roll) % 10 if (self.pos + roll) % 10 else 10
            score = self.score + pos
            if score >= 21:
                wins += ct
            else:
                new_players.append((Player(self.id, pos, score), ct))
        return new_players, wins


@dataclass
class Game:
    p1: Player
    p2: Player
    weight: int = field(default=1, compare=False)

    def play_turn(self) -> tuple[list[Game], int]:
        new_players, wins = self.p1.roll()
        return [Game(self.p2, player, weight * self.weight) for player, weight in new_players], wins * self.weight


def compute(s: str) -> int:
    games = [Game(*(Player.create(line) for line in s.splitlines()))]
    wins = collections.Counter()

    while len(games):
        game = games.pop()
        new_games, win = game.play_turn()
        wins[game.p1.id] += win
        games.extend(new_games)
    return wins.most_common()[0][1]


INPUT_S = '''\
Player 1 starting position: 4
Player 2 starting position: 8
'''
EXPECTED = 444356092776315


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
