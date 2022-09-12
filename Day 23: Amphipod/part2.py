from __future__ import annotations

import argparse
import heapq
import os.path
import re
from copy import deepcopy
from dataclasses import dataclass

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


@dataclass(frozen=True)
class Burrow:
    top: dict[int, int | None]
    p: dict[int, dict[int, int | None]]

    def __hash__(self) -> int:
        return hash((
            tuple(self.top.items()),
            tuple(self.p[1].items()),
            tuple(self.p[2].items()),
            tuple(self.p[3].items()),
            tuple(self.p[4].items()),
        ))

    def __lt__(self, other: Burrow) -> bool:
        return True

    @property
    def done(self) -> bool:
        return all(k == v for p in self.p.values() for k, v in p.items())

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
                for i in range(len(self.p), 0, -1):
                    if self.p[i][v] is None and all(self.p[j + 1][v] == v for j in range(i, len(self.p))):
                        new_states.append((
                            (to_move_top + i) * 10 ** v,
                            self._replace(t=(k, None), row=(i, (v, v)))
                        ))
                        break

        potential_targets = {k for k, v in self.top.items() if v is None}
        for i in range(len(self.p)):
            p_vals = [self.p[j][i] for j in range(1, len(self.p) + 1)]
            # this row is done! do not move!
            if all(val == i for val in p_vals):
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
                    for j in range(len(self.p)):
                        if (
                                all(val is None for val in p_vals[:j]) and
                                p_vals[j] is not None and
                                any(val != i for val in p_vals[j:])
                        ):
                            new_states.append((
                                (to_move_top + j + 1) * 10 ** p_vals[j],
                                self._replace(t=(target, self.p[j + 1][i]), row=(j + 1, (i, None))),
                            ))
                            break
        return new_states

    @classmethod
    def create(cls, input_txt: str) -> Burrow:
        conversion_dict = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
        p1 = re.findall(r'[A-Z]', input_txt.splitlines()[2])
        p2 = re.findall(r'[A-Z]', '#D#C#B#A#')
        p3 = re.findall(r'[A-Z]', '#D#B#A#C#')
        p4 = re.findall(r'[A-Z]', input_txt.splitlines()[3])
        return cls(
            top=dict.fromkeys((0, 1, 3, 5, 7, 9, 10), None),
            p={i + 1: {k: conversion_dict[v] for k, v in enumerate(p)} for i, p in enumerate((p1, p2, p3, p4))}
        )

    def _replace(self, t: tuple[int, int | None], row: tuple[int, tuple[int, int | None]]) -> Burrow:
        top = deepcopy(self.top)
        top[t[0]] = t[1]
        p = deepcopy(self.p)
        p[row[0]][row[1][0]] = row[1][1]
        return Burrow(top=top, p=p)


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
EXPECTED = 44169


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
