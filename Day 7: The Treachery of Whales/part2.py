import numpy as np

positions = np.array([int(x) for x in open("input.txt").readline().split(',')])
# positions = np.array([16, 1, 2, 0, 4, 2, 7, 1, 2, 14])


def move(coordinates: np.ndarray, pos: int) -> int:
    fuel_sum = 0
    for i in range(len(coordinates)):
        fuel_sum += pos - coordinates[i]
    return fuel_sum


def find_pos(coordinates: np.ndarray) -> int:
    pos = 0
    while True:
        delta_fuel = move(coordinates, pos)
        if delta_fuel < 0:
            pos += 1
        else:
            return pos
        print(pos)


def calc_fuel(coordinates: np.ndarray, pos: int) -> int:
    fuel_total = 0
    for coord in coordinates:
        crab_total = 0
        for rate in range(abs(pos - coord)):
            crab_total += rate + 1
        fuel_total += crab_total
    return fuel_total


optimal_pos = find_pos(positions)
print(optimal_pos, calc_fuel(positions, optimal_pos))
print(optimal_pos, calc_fuel(positions, optimal_pos-1))
print(optimal_pos, calc_fuel(positions, optimal_pos-2))
