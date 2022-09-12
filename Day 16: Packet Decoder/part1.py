from __future__ import annotations

import argparse
import chunk
import os.path

import pytest

import support
from numpy import product

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class Packet:
    def __init__(self, bin_str, i):
        self.i = i
        self.bin = bin_str
        self.version = self._read(3)
        self.id = self._read(3)

    def parse(self) -> tuple[int, str, int]:
        if self.id == 4:
            return self.parse_literal()
        else:
            return self.parse_subpackets()

    def parse_literal(self) -> tuple[int, str, int]:
        chunk = self._read(5)
        n = chunk & 0b1111
        while chunk & 0b10000:
            chunk = self._read(5)
            n <<= 4
            n += chunk & 0b1111
        return self.version, self.bin[self.i:], n

    def parse_subpackets(self) -> tuple[int, str, int]:
        version_sum = self.version
        values = []
        if self._read(1) == 0:
            sub_packet_length = self._read(15)
            rest = self.bin[7 + 15:7 + 15 + sub_packet_length]
            while rest:
                sub_packet = Packet(rest, 0)
                version, rest, value = sub_packet.parse()
                values.append(value)
            rest = self.bin[7 + 15 + sub_packet_length:]
        else:
            sub_packet_number = self._read(11)
            rest = self.bin[7 + 11:]
            for _ in range(sub_packet_number):
                assert rest != '', 'no rest'
                sub_packet = Packet(rest, 0)
                version, rest, value = sub_packet.parse()
                values.append(value)
        if self.id == 0:
            value = sum(values)
        elif self.id == 1:
            value = product(values)
        elif self.id == 2:
            value = min(values)
        elif self.id == 3:
            value = max(values)
        elif self.id == 5:
            value = values[0] > values[1]
        elif self.id == 6:
            value = values[0] < values[1]
        elif self.id == 7:
            value = values[0] == values[1]
        return version_sum, rest, value

    def _read(self, n: int) -> int:
        ret = int(self.bin[self.i:self.i + n], 2)
        self.i += n
        return ret


def compute(s: str) -> int:
    bin_str = ''
    for c in s.strip():
        bin_str += f'{int(c, 16):04b}'

    packet = Packet(bin_str, 0)

    return packet.parse()[2]


INPUT_S = '''\
C200B40A82
'''
EXPECTED = 3
INPUT_S1 = '''\
04005AC33890
'''
EXPECTED1 = 54
INPUT_S2 = '''\
880086C3E88112
'''
EXPECTED2 = 7
INPUT_S3 = '''\
D8005AC2A8F0
'''
EXPECTED3 = 1
INPUT_S4 = '''\
F600BC2D8F
'''
EXPECTED4 = 0
INPUT_S5 = '''\
9C005AC2F8F0
'''
EXPECTED5 = 0
INPUT_S6 = '''\
9C0141080250320F1802104A08
'''
EXPECTED6 = 1


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, EXPECTED),
            (INPUT_S1, EXPECTED1),
            (INPUT_S2, EXPECTED2),
            (INPUT_S3, EXPECTED3),
            (INPUT_S4, EXPECTED4),
            (INPUT_S5, EXPECTED5),
            (INPUT_S6, EXPECTED6),
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
