from __future__ import annotations

import argparse
import os.path
import re

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

bounds = (-50, 50)


def compute(s: str) -> int:
    on: set[tuple[int, int, int]] = set()
    lines = s.splitlines()
    for line in lines:
        x_min, x_max, y_min, y_max, z_min, z_max = (int(x) for x in re.findall(r'-?\d+', line))
        x_min, x_max, y_min, y_max, z_min, z_max = \
            max(x_min, bounds[0]), min(x_max, bounds[1]), max(y_min, bounds[0]), \
            min(y_max, bounds[1]), max(z_min, bounds[0]), min(z_max, bounds[1])

        cuboid = set((x, y, z) for x in range(x_min, x_max + 1) for y in range(y_min, y_max + 1) for z in
                     range(z_min, z_max + 1))
        if line[:2] == 'on':
            on |= cuboid
        elif line[:3] == 'off':
            on -= cuboid
    return len(on)


INPUT_S = '''\
on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
on x=10..10,y=10..10,z=10..10
'''
EXPECTED = 39
INPUT_S2 = '''\
on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682
'''
EXPECTED2 = 590784


# noinspection DuplicatedCode
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, EXPECTED),
            (INPUT_S2, EXPECTED2),
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
