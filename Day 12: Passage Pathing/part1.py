from __future__ import annotations

from copy import copy
from itertools import chain

from cave import Cave, import_caves


def loop(start):
    paths: list[list[Cave]] = [[start]]
    while paths:
        new_paths = [extend_options(path) for path in paths if path[-1].name != 'end']
        paths = list(chain(*new_paths))


def extend_options(path: list[Cave]) -> list[list[Cave]]:
    global successfull
    newpaths: list[list[Cave]] = []
    for cave in path[-1].adjacent:
        if not (cave.small and cave.visits) and cave.name not in [scave.name for scave in path if scave.small]:
            newpaths.append(copy(path))
            newpaths[-1].append(copy(cave))
            newpaths[-1][-1].visits += 1
            if newpaths[-1][-1].name == 'end':
                successfull += 1
    return newpaths


if __name__ == '__main__':
    successfull = 0
    caves = import_caves('input.txt')
    loop(caves['start'])
    print(successfull)
