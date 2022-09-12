import re


def import_file(path: str = 'input.txt') -> tuple[list[list[int, int]], list[tuple[str, int]]]:
    with open(path) as f:
        text = f.read()
        coordinates = re.findall(r'^([0-9]+),([0-9]+)', text, re.MULTILINE)
        folds = re.findall(r'^fold along ([xy])=([0-9]+)', text, re.MULTILINE)

        coordinates = [[int(coord[0]), int(coord[1])] for coord in coordinates]
        folds = [(fold[0], int(fold[1])) for fold in folds]

        return coordinates, folds


def fold_coord(coord: list[int, int], axis: str, position: int) -> list[int, int]:
    index = 0 if axis == 'x' else 1
    if coord[index] == position:
        raise "coord on fold"
    elif coord[index] > position:
        coord[index] = 2 * position - coord[index]
    return coord


def fold_all(coords, fold):
    coords = [fold_coord(coord, fold[0], fold[1]) for coord in coords]
    new_coords = []
    for elem in coords:
        if elem not in new_coords:
            new_coords.append(elem)
    return new_coords


def show_field(coords):
    size = max([coord[0] for coord in coords]) + 1, max([coord[1] for coord in coords]) + 1
    field = [['.'] * size[0] for _ in range(size[1])]
    for coord in coords:
        field[coord[1]][coord[0]] = 'x'
    for row in field:
        print(' '.join(row))

if __name__ == '__main__':
    coords, folds = import_file()
    show_field(coords)
    for fold in folds:
        print()
        coords = fold_all(coords, fold)
        show_field(coords)
