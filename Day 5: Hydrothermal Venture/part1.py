import numpy as np

with open("input.txt", "r") as f:
    lines = f.readlines()
    coordinates = []
    max_x, max_y = 0, 0
    for line in lines:
        command = line.split(" -> ")
        lst = []
        for coordinate in command:
            x, y = [int(n) for n in coordinate.split(",")]
            lst.append((x, y))
            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y
        coordinates.append(lst)


def interpolate(co1: tuple[int], co2: tuple[int]) -> list[tuple[int, int]]:
    if co1[0] == co2[0]:
        x = co1[0]
        ys = range(min(co1[1], co2[1]), max(co1[1], co2[1]) + 1)
        return [(x, y) for y in ys]
    elif co1[1] == co2[1]:
        y = co1[1]
        xs = range(min(co1[0], co2[0]), max(co1[0], co2[0]) + 1)
        return [(x, y) for x in xs]
    else:
        # raise ValueError(f"not a strait line: from {co1} to {co2}")
        return None


def mark_vents(coordinates: list) -> list:
    vents = []
    for line in coordinates:
        try:
            for coordinate in interpolate(*line):
                vents.append(coordinate)
        except TypeError:
            pass
    return vents


class Field:
    def __init__(self, x, y):
        self.array = np.zeros((x, y))

    def mark(self, coordinate):
        self.array[coordinate] += 1

    def count_threshold(self, n):
        return len(self.array[self.array >= n])


if __name__ == '__main__':
    field = Field(max_x + 1, max_y + 1)
    vents = mark_vents(coordinates)
    for vent in vents:
        field.mark(vent)
    print(field.count_threshold(2))
