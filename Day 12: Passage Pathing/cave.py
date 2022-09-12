from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class Cave:
    name: str
    small: bool = field(default=False)
    adjacent: list[Cave] = field(default_factory=list)

    def __repr__(self):
        return self.name


def import_caves(file: str = 'input.txt') -> dict[str, Cave]:
    with open(file) as f:
        pairs = re.findall(r'^([a-zA-Z]+)-([a-zA-Z]+)', f.read(), re.MULTILINE)
    cavedict: dict[str, Cave] = {}
    for pair in pairs:
        for newcave in pair:
            if newcave not in cavedict.keys():
                cavedict[newcave] = (Cave(newcave, newcave.islower()))
        cavedict[pair[0]].adjacent.append(cavedict[pair[1]])
        cavedict[pair[1]].adjacent.append(cavedict[pair[0]])
    return cavedict
