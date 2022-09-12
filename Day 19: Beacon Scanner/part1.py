from __future__ import annotations

import argparse
import collections
import os.path
from dataclasses import dataclass

import pytest

import support
from itertools import permutations

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


@dataclass
class Axis:
    ax: int
    sign: int
    div: int


@dataclass
class Scanner:
    id: int
    axi: list[Axis | None]
    detected_beacons: set[tuple[int, int, int]]

    @property
    def absolute_beacons(self) -> set[tuple[int, int, int]]:
        return set(tuple(coord[axis.ax] * axis.sign + axis.div for axis in self.axi) for coord in self.detected_beacons)

    def match(self, other: Scanner) -> bool:
        if None in other.axi:
            return True
        elif not (None in self.axi):
            return False
        axes = tuple(i for i, a in enumerate(self.axi) if a is None)
        for ax in axes:
            for sign in (-1, 1):
                d = {i: collections.Counter() for i in (0, 1, 2)}
                for x, y, z in other.absolute_beacons:
                    for choord in self.detected_beacons:
                        d[0][x - choord[ax] * sign] += 1
                        d[1][y - choord[ax] * sign] += 1
                        d[2][z - choord[ax] * sign] += 1
                for axis in axes:
                    (diff, n), = d[axis].most_common(1)
                    if n >= 12 and self.axi[axis] is None:
                        self.axi[axis] = Axis(ax, sign, diff)
        return True if None in self.axi else False


def compute(s: str) -> int:
    scanner_strs = s.split('\n\n')
    scanners = []
    for i, str in enumerate(scanner_strs):
        scanners.append(Scanner(
            i, [None, None, None],
            set(tuple(int(c) for c in line.split(',')) for line in str.splitlines()[1:])
        ))
    scanners[0].axi = [Axis(i, 1, 0) for i in range(3)]
    known_beacons = set(scanners[0].absolute_beacons)

    run = True
    while run:
        run = False
        for scanner, other in permutations(scanners, 2):
            if scanner.match(other):
                run = True

    for scanner in scanners:
        known_beacons.update(scanner.absolute_beacons)

    return len(known_beacons)


INPUT_S = '''\
--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14
'''
EXPECTED = 79


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
