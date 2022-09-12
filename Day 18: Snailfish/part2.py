from __future__ import annotations

import argparse
import ast
import os.path
import re
from itertools import permutations
from math import floor, ceil
from typing import Any

import pytest
import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

PAIR_RE = re.compile(r'\[(\d+),(\d+)\]')
NUM_RE = re.compile(r'\d+')
GT_10 = re.compile(r'\d\d+')


def add_number(s1, s2):
    return f'[{s1},{s2}]'


def reduce(s) -> str:
    while True:
        again = False
        for found in PAIR_RE.finditer(s):
            if len(re.findall(r'\[', s[:found.regs[0][0]])) - len(re.findall(r'\]', s[:found.regs[0][0]])) >= 4:
                d_len = 0
                if f_num := NUM_RE.search(s[found.regs[0][0]::-1]):
                    i_max = found.regs[0][0] - f_num.regs[0][0] + 1
                    i_min = found.regs[0][0] - f_num.regs[0][1] + 1
                    s_len = len(s)
                    s = s[:i_min] + str(int(s[i_min:i_max]) + int(s[found.regs[1][0]:found.regs[1][1]])) + s[i_max:]
                    d_len = len(s) - s_len
                if f_num := NUM_RE.search(s[found.regs[0][1]:]):
                    i_min = found.regs[0][1] + f_num.regs[0][0]
                    i_max = found.regs[0][1] + f_num.regs[0][1]
                    s = s[:i_min] + str(
                        int(s[i_min:i_max]) + int(s[found.regs[2][0] + d_len:found.regs[2][1] + d_len])) + s[i_max:]
                s = s[:found.regs[0][0]+d_len] + '0' + s[found.regs[0][1]+d_len:]
                again = True
                break

        if not again:
            if found := GT_10.search(s):
                num = int(s[found.regs[0][0]:found.regs[0][0] + 2])
                num_str = f'[{floor(num / 2)},{ceil(num / 2)}]'
                s = s[:found.regs[0][0]] + num_str + s[found.regs[0][0] + 2:]
            else:
                return s


def compute_sum(s: str) -> int:
    def compute_val(v: int | Any) -> int:
        if isinstance(v, int):
            return v
        else:
            assert len(v) == 2
            return 3 * compute_val(v[0]) + 2 * compute_val(v[1])

    return compute_val(ast.literal_eval(s))


def compute(s: str) -> int:
    lines = s.splitlines()
    max_sum = 0
    for combi in permutations(lines, 2):
        max_sum = max(max_sum, compute_sum(reduce(add_number(*combi))))
    return max_sum


# noinspection DuplicatedCode
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
EXPECTED = 3993


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
