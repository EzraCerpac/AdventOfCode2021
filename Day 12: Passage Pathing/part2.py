from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from itertools import chain

from cave import Cave, import_caves


@dataclass
class Path:
    path: list[Cave] = field(default_factory=list)
    double_cave: Cave = field(default=None)

    def append_cave(self, cave: Cave):
        if cave.name in [scave.name for scave in self.path if scave.small]:
            if not self.double_cave and cave.name not in ("start", "end"):
                self.double_cave = cave
            else:
                raise EnvironmentError('Not possible to travel to this cave')
        self.path.append(cave)


def loop(start: Cave):
    paths: list[Path] = [Path([start])]
    while paths:
        new_paths = [extend_options(path) for path in paths if path.path[-1].name != 'end']
        paths = list(chain(*new_paths))


def extend_options(path: Path) -> list[Path]:
    global successfull
    newpaths: list[Path] = []
    for cave in path.path[-1].adjacent:
        newpaths.append(deepcopy(path))
        try:
            newpaths[-1].append_cave(cave)
            if newpaths[-1].path[-1].name == 'end':
                successfull += 1
                print(successfull, newpaths[-1])
        except EnvironmentError:
            del newpaths[-1]
    return newpaths


if __name__ == '__main__':
    successfull = 0
    caves = import_caves('input.txt')
    loop(caves['start'])
    print(successfull)
