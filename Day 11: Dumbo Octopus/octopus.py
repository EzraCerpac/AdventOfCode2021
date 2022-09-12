class Octopus:
    def __init__(self, energy: int):
        self.energy = energy
        self.flash = False
        self.flashed = False

    def append_one(self) -> None:
        self.energy += 1
        if self.energy >= 10 and not self.flashed:
            self.flash = True

    def reset(self):
        if self.flashed:
            self.flashed = False
            self.energy = 0
        if self.flash:
            raise EnvironmentError("Missed Flash")


class Field:
    def __init__(self, file):
        self.flash_count = 0
        self.flash_n = 0
        n_map = self.read_file(file)
        self.octo_map: list[list[Octopus]] = []
        for line in n_map:
            octo_line = []
            for n in line:
                octo_line.append(Octopus(n))
            self.octo_map.append(octo_line)

    def progress(self, n=1):
        for step in range(n):
            for octo_line in self.octo_map:
                for octopus in octo_line:
                    octopus.append_one()
            self.check_flash()
            self.reset_energy()
            if self.flash_n == 100:
                print(f"simultaneous flash in step {step + 1}")
            elif self.flash_n < 100:
                self.flash_n = 0

    def check_flash(self) -> None:
        change = True
        while change:
            change = False
            for j, octo_line in enumerate(self.octo_map):
                for i, octopus in enumerate(octo_line):
                    if octopus.flash:
                        self.flash_count += 1
                        self.flash_n += 1
                        octopus.flashed = True
                        octopus.flash = False
                        self.spread_energy(i, j)
                        change = True

    def spread_energy(self, x: int, y: int) -> None:
        xs = [n for n in [x - 1, x, x + 1] if n >= 0]
        ys = [n for n in [y - 1, y, y + 1] if n >= 0]
        for i in xs:
            for j in ys:
                try:
                    self.octo_map[j][i].append_one()
                except IndexError:
                    pass

    def reset_energy(self):
        for octo_line in self.octo_map:
            for octopus in octo_line:
                octopus.reset()

    def print_map(self):
        for octo_line in self.octo_map:
            line = []
            for octopus in octo_line:
                line.append(octopus.energy)
            print(line)

    @staticmethod
    def read_file(file) -> list[list[int]]:
        lines = [line.strip('\n') for line in open(file).readlines()]
        n_map = []
        for line in lines:
            n_line = []
            for n in line:
                n_line.append(int(n))
            n_map.append(n_line)
        return n_map


