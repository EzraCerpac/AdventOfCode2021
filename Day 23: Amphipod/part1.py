from __future__ import annotations

import argparse
import heapq
import os.path
import re
from dataclasses import dataclass
from enum import Enum
from typing import ClassVar

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


@dataclass(frozen=True)
class Burrow:
    top: dict[int, int | None]
    p1: dict[int, int | None]
    p2: dict[int, int | None]

    def __hash__(self) -> int:
        return hash((
            tuple(self.top.items()),
            tuple(self.p1.items()),
            tuple(self.p2.items()),
        ))

    def __lt__(self, other: Burrow) -> bool:
        return True

    @property
    def done(self) -> bool:
        return all(k == v for k, v in self.p1.items()) and all(k == v for k, v in self.p2.items())

    def all_moves(self) -> list[tuple[int, Burrow]]:  # from anthonywritescode
        new_states = []
        for k, v in self.top.items():
            if v is None:
                continue

            target_col = 2 + v * 2
            max_c = max(target_col, k)
            min_c = min(target_col, k)
            to_move_top = max_c - min_c

            if all(
                    k2 <= min_c or k2 >= max_c or v2 is None
                    for k2, v2 in self.top.items()
            ):
                if self.p2[v] is None:
                    new_states.append(
                        ((to_move_top + 2) * 10 ** v,
                         self._replace(
                             top={**self.top, k: None},
                             p2={**self.p2, v: v},
                         )
                         ))
                elif self.p2[v] == v and self.p1[v] is None:
                    new_states.append(
                        ((to_move_top + 1) * 10 ** v,
                         self._replace(
                             top={**self.top, k: None},
                             p1={**self.p1, v: v},
                         ),
                         ))

        potential_targets = {k for k, v in self.top.items() if v is None}
        for i in range(4):
            p1_val = self.p1[i]
            p2_val = self.p2[i]
            # this row is done! do not move!
            if p1_val == i and p2_val == i:
                continue

            for target in potential_targets:
                src_col = 2 + i * 2
                max_c = max(src_col, target)
                min_c = min(src_col, target)
                to_move_top = max_c - min_c

                if all(
                        k2 <= min_c or k2 >= max_c or v2 is None
                        for k2, v2 in self.top.items()
                ):
                    if p1_val is not None:
                        new_states.append(
                            ((to_move_top + 1) * 10 ** p1_val,
                             self._replace(
                                 top={**self.top, target: p1_val},
                                 p1={**self.p1, i: None},
                             )
                             ))
                    elif p2_val != i and p2_val is not None:
                        new_states.append(
                            ((to_move_top + 2) * 10 ** p2_val,
                             self._replace(
                                 top={**self.top, target: p2_val},
                                 p2={**self.p2, i: None},
                             ),
                             ))
        return new_states

    @classmethod
    def create(cls, input_txt: str) -> Burrow:
        conversion_dict = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
        p1 = re.findall(r'[A-Z]', input_txt.splitlines()[2])
        p2 = re.findall(r'[A-Z]', input_txt.splitlines()[3])
        return cls(
            top=dict.fromkeys((0, 1, 3, 5, 7, 9, 10), None),
            p1={k: conversion_dict[v] for k, v in enumerate(p1)},
            p2={k: conversion_dict[v] for k, v in enumerate(p2)},
        )

    def _replace(self, **attrs) -> Burrow:
        return Burrow(**{k: v for k, v in attrs.items() if v is not None},
                      **{k: v for k, v in self.__dict__.items() if k not in attrs})


def compute(s: str) -> int:
    seen = set()
    todo = [(0, Burrow.create(s))]
    while todo:
        score, burrow = heapq.heappop(todo)
        if burrow.done:
            return score
        if burrow in seen:
            continue
        seen.add(burrow)
        for d_score, state in burrow.all_moves():
            heapq.heappush(todo, (score + d_score, state))
    raise ValueError('No solution found')


INPUT_S = '''\
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
'''
EXPECTED = 12521


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
