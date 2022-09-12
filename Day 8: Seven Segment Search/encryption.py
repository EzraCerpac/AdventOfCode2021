from collections import Counter
from itertools import product
from typing import Optional


class Encryption:
    def __init__(self, signal):
        self.segments = {
            "top": {chr(i) for i in range(97, 104)},
            "top_left": {chr(i) for i in range(97, 104)},
            "top_right": {chr(i) for i in range(97, 104)},
            "mid": {chr(i) for i in range(97, 104)},
            "bottom": {chr(i) for i in range(97, 104)},
            "bottom_left": {chr(i) for i in range(97, 104)},
            "bottom_right": {chr(i) for i in range(97, 104)}
        }

        self.number_dict = {
            0: {"top", "top_left", "top_right", "bottom", "bottom_left", "bottom_right"},
            1: {"top_right", "bottom_right"},
            2: {"top", "top_right", "mid", "bottom_left", "bottom"},
            3: {"top", "top_right", "mid", "bottom_right", "bottom"},
            4: {"top_left", "mid", "top_right", "bottom_right"},
            5: {"top", "top_left", "mid", "bottom_right", "bottom"},
            6: {"top", "top_left", "mid", "bottom_right", "bottom", "bottom_left"},
            7: {"top", "top_right", "bottom_right"},
            8: {"top", "top_left", "top_right", "mid", "bottom", "bottom_left", "bottom_right"},
            9: {"top", "top_left", "top_right", "mid", "bottom", "bottom_right"}
        }

        for number in signal:
            if len(number) in [2, 3, 4, 7]:
                self.filter_options(number)
        self.solve()
        self.try_options(signal)

    def filter_options(self, signal: str) -> None:
        mapping = {2: 1, 3: 7, 4: 4, 7: 8}
        n_disp = mapping[len(signal)]
        for position in self.number_dict[n_disp]:
            self.segments[position] = set(filter(lambda a: a in signal, self.segments[position]))

    def solve(self):
        done = False
        while not done:
            done = True
            freqs = Counter(frozenset(options) for options in self.segments.values())
            for set, freq in freqs.items():
                if len(set) == freq:
                    for segment in self.segments.values():
                        if segment != set:
                            for letter in set:
                                try:
                                    segment.remove(letter)
                                    done = False
                                except KeyError:
                                    pass

    @property
    def segments_inv(self) -> dict[str, str]:
        return {next(iter(v)): k for k, v in self.segments.items()}

    def output(self, signal: str) -> Optional[int]:
        active_segments = set()
        for letter in signal:
            try:
                active_segments.add(self.segments_inv[letter])
            except KeyError:
                return None
        for number, segments in self.number_dict.items():
            if active_segments == segments:
                return number
        return None

    def try_options(self, signal_list: list[str]):
        segment_list = [list(x) for x in self.segments.values()]
        options = list(product(*segment_list))
        for option in options:
            fail = False
            for i, key in enumerate(self.segments.keys()):
                self.segments[key] = option[i]
            for signal in signal_list:
                if self.output(signal) == None:
                    fail = True
            if not fail:
                return
        raise EnvironmentError("no good option found")

    def calc_value(self, signal_list: list[str]) -> int:
        value_str = []
        for signal in signal_list:
            value_str.append(str(self.output(signal)))
        return int(''.join(value_str))
