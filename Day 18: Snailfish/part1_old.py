from __future__ import annotations

import argparse
import os.path
import re
from abc import ABC
from collections import namedtuple
from dataclasses import dataclass
from math import floor, ceil
from typing import Union, Optional, Protocol

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class _number(ABC):
    def __repr__(self) -> str:
        ...

    @property
    def magnitude(self) -> int:
        ...

    def nested(self, depth):
        ...

    def split(self) -> bool | Number:
        ...

    def explode(self):
        ...


@dataclass
class regNumber(_number):
    value: int

    def __repr__(self) -> str:
        return str(self.value)

    @property
    def magnitude(self) -> int:
        return self.value

    def nested(self, depth):
        return None

    def split(self) -> bool | Number:
        if self.value >= 10:
            return Number(regNumber(floor(self.value/2)), regNumber(ceil(self.value/2)))
        else:
            return False

    def explode(self):
        pass

@dataclass
class Number(_number):
    left: _number
    right: _number

    def __repr__(self) -> str:
        return f'[{self.left},{self.right}]'

    @property
    def magnitude(self) -> int:
        return 3 * self.left.magnitude + 2 * self.right.magnitude

    @classmethod
    def create(cls, s) -> Number:
        assert s[0] == '[' and s[-1] == ']', 'not a snailfish number'
        bracket_count = -1
        for i, c in enumerate(s):
            bracket_count += c == '['
            bracket_count -= c == ']'
            if c == ',' and not bracket_count:
                try:
                    left = regNumber(int(s[1:i]))
                except ValueError:
                    left = cls.create(s[1:i])
                try:
                    right = regNumber(int(s[1+i:-1]))
                except ValueError:
                    right = cls.create(s[1+i:-1])
                return cls(left, right)

    def nested(self, depth):
        if self.left is Number:
            self.left.nested(depth + 1)
        if self.left is Number:
            self.left.nested(depth + 1)
        if depth >= 4:
            self.explode()

    def split(self) -> bool | Number:
        if l := self.left.split():
            self.left = l
            reduce()
        elif r := self.right.split():
            self.right = r
            reduce()

    def explode(self):
        pass


def reduce():
    pass


def compute(s: str) -> int:
    lines = s.splitlines()
    for line in lines:
        print(Number.create(line))
    # TODO: implement solution here!
    return 0


INPUT_S = '''\
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
'''
EXPECTED = 4140


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
