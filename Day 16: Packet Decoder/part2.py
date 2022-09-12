from __future__ import annotations

import argparse
import chunk
import os.path

import pytest

import support


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
        value_sum = 0
        if self._read(1) == 0:
            sub_packet_length = self._read(15)
            rest = self.bin[7 + 15:7 + 15 + sub_packet_length]
            while rest:
                sub_packet = Packet(rest, 0)
                version, rest, value = sub_packet.parse()
                version_sum += version
            rest = self.bin[7 + 15 + sub_packet_length:]
        else:
            sub_packet_number = self._read(11)
            rest = self.bin[7 + 11:]
            for _ in range(sub_packet_number):
                assert rest != '', 'no rest'
                sub_packet = Packet(rest, 0)
                version, rest, value = sub_packet.parse()
                version_sum += version
        return version_sum, rest, value_sum

    def _read(self, n: int) -> int:
        ret = int(self.bin[self.i:self.i + n], 2)
        self.i += n
        return ret


def compute(s: str) -> int:
    bin_str = ''
    for c in s.strip():
        bin_str += f'{int(c, 16):04b}'

    packet = Packet(bin_str, 0)

    return packet.parse()[0]


INPUT_S = '''\
D2FE28
'''
EXPECTED = 2021
INPUT_S1 = '''\
8A004A801A8002F478
'''
EXPECTED1 = 16
INPUT_S2 = '''\
620080001611562C8802118E34
'''
EXPECTED2 = 12
INPUT_S3 = '''\
C0015000016115A2E0802F182340
'''
EXPECTED3 = 23
INPUT_S4 = '''\
A0016C880162017C3686B18A3D4780
'''
EXPECTED4 = 31


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            # (INPUT_S, EXPECTED),
            (INPUT_S1, EXPECTED1),
            (INPUT_S2, EXPECTED2),
            (INPUT_S3, EXPECTED3),
            (INPUT_S4, EXPECTED4),
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
