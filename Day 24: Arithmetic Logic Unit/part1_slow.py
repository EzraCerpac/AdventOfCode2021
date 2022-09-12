from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class ALU:
    def __init__(self, model: int):
        self.w, self.x, self.y, self.z = 0, 0, 0, 0
        self.i = 0
        self.model = str(model)

    def run_command(self, command: str) -> None:
        match command.split():
            case ['inp', var]:
                self.__dict__[var] = int(self.model[self.i])
                self.i += 1
            case ['add', var1, var2]:
                if var2[-1].isdigit():
                    self.__dict__[var1] += int(var2)
                else:
                    self.__dict__[var1] += self.__dict__[var2]
            case ['mul', var1, var2]:
                if var2[-1].isdigit():
                    self.__dict__[var1] *= int(var2)
                else:
                    self.__dict__[var1] *= self.__dict__[var2]
            case ['div', var1, var2]:
                if var2[-1].isdigit():
                    self.__dict__[var1] //= int(var2)
                else:
                    self.__dict__[var1] //= self.__dict__[var2]
            case ['mod', var1, var2]:
                if var2[-1].isdigit():
                    self.__dict__[var1] %= int(var2)
                else:
                    self.__dict__[var1] %= self.__dict__[var2]
            case ['eql', var1, var2]:
                if var2[-1].isdigit():
                    self.__dict__[var1] = self.__dict__[var1] == int(var2)
                else:
                    self.__dict__[var1] = self.__dict__[var1] == self.__dict__[var2]


def compute(s: str) -> int:
    n_start = int(1e14 - 1)
    for n in range(n_start, 0, -1):
        if '0' in str(n):
            continue
        alu = ALU(n)
        for line in s.splitlines():
            alu.run_command(line)
        if alu.z == 0:
            return n


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
