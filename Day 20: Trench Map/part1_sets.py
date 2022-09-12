from __future__ import annotations

import argparse
import collections
import os.path
from dataclasses import dataclass

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


@dataclass
class Image:
    field: set[tuple[int, int]]
    alg: str
    rest: bool

    def __post_init__(self) -> None:
        self.min_x = min(x for x, _ in self.field) - 1
        self.max_x = max(x for x, _ in self.field) + 1
        self.min_y = min(y for _, y in self.field) - 1
        self.max_y = max(y for _, y in self.field) + 1

    @property
    def n_lit(self) -> int:
        return len(self.field)

    @classmethod
    def create(cls, s, alg) -> Image:
        return cls(support.parse_coords_hash(s), alg, False)

    def enhance(self) -> Image:
        return Image(
            self._new_field(self._enhance_all()),
            self.alg,
            not self.rest if self.alg[0] == '#' else False  # TODO: should stay True cause 9
        )

    def _in_bound(self, coord: tuple[int, int]) -> bool:
        return self.min_x <= coord[0] <= self.max_x and self.min_y <= coord[1] <= self.max_y

    def _enhance_pixel(self, coord: tuple[int, int]) -> int:
        n = 0
        for row in (coord[1] - 1, coord[1], coord[1] + 1):
            for column in (coord[0] - 1, coord[0], coord[0] + 1):
                pos = (column, row)
                n <<= 1
                n += pos in self.field or (not self._in_bound(pos) and self.rest)
        return n

    def _enhance_all(self) -> dict[tuple[int, int], int]:
        return {(x, y): self._enhance_pixel((x, y))
                for x in range(self.min_x, self.max_x + 1)
                for y in range(self.min_y, self.max_y + 1)}

    def _new_field(self, enhance_dict: dict[tuple[int, int], int]) -> set[tuple[int, int]]:
        return set([(x, y) for (x, y), n in enhance_dict.items() if self.alg[n] == '#'])

    def __str__(self) -> str:
        return support.format_coords_hash(self.field)


def compute(s: str) -> int:
    alg, img_str = s.split('\n\n')
    img = Image.create(img_str, alg)
    print(img)
    for _ in range(2):
        print()
        img = img.enhance()
        print(img)
    return img.n_lit


INPUT_S = '''\
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##\
#..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###\
.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#.\
.#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#.....\
.#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#..\
...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.....\
..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
'''
EXPECTED = 35


# # noinspection DuplicatedCode
# @pytest.mark.parametrize(
#     ('input_s', 'expected'),
#     (
#             (INPUT_S, EXPECTED),
#     ),
# )
# def test(input_s: str, expected: int) -> None:
#     assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
