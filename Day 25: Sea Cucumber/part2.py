from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    sea = s.splitlines()
    SIZE = (len(sea[0]), len(sea))

    def next(pos: tuple[int, int], east: bool) -> (int, int):
        x, y = pos
        if east:
            x = (x + 1) % SIZE[0]
        else:
            y = (y + 1) % SIZE[1]
        return x, y

    east: set[tuple[int, int]] = set()
    south: set[tuple[int, int]] = set()
    for y, row in enumerate(sea):
        for x, c in enumerate(row):
            if c == '>':
                east.add((x, y))
            elif c == 'v':
                south.add((x, y))
            elif c != '.':
                raise ValueError(f'invalid character: {c}')

    def is_empty(pos: tuple[int, int]) -> bool:
        return not (pos in east or pos in south)

    run = True
    steps = 0
    while run:
        steps += 1
        m_east: set[tuple[int, int]] = set()
        m_south: set[tuple[int, int]] = set()
        for cucumber in east:
            if is_empty(next(cucumber, True)):
                m_east.add(cucumber)
        for cucumber in m_east:
            east.remove(cucumber)
            east.add(next(cucumber, True))
        for cucumber in south:
            if is_empty(next(cucumber, False)):
                m_south.add(cucumber)
        for cucumber in m_south:
            south.remove(cucumber)
            south.add(next(cucumber, False))
        if not m_east and not m_south:
            run = False

    return steps


INPUT_S = '''\
v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>
'''
EXPECTED = 58


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
