from __future__ import annotations

import argparse
import os.path
import re

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    x_min, x_max, y_min, y_max = [int(n) for n in re.findall(r'target area: x=(\d+)..(\d+), y=(-?\d+)..(-?\d+)', s)[0]]

    def max_height(vy: int) -> int:
        return sum(i for i in range(vy + 1))

    vy = -y_min - 1

    return max_height(vy)


INPUT_S = '''\
target area: x=20..30, y=-10..-5
'''
EXPECTED = 45


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
