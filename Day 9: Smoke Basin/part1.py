from typing import List, Any

rows = [row.strip('\n') for row in open("input.txt").readlines()]
field: list[list[int]] = []
for row in rows:
    field.append([int(n) for n in row])

visited_type = list[tuple[int, int]]


def extract_window(x: int, y: int, matrix: field):
    if (x, y) == (0, 0):
        return [matrix[x + 1][y], matrix[x][y + 1]]
    elif (x, y) == (len(matrix) - 1, len(matrix[0]) - 1):
        return [matrix[x - 1][y], matrix[x - 1][y - 1]]
    elif (x, y) == (0, len(matrix[0]) - 1):
        return [matrix[x][y - 1], matrix[x + 1][y]]
    elif y == len(matrix[0]) - 1:
        return [matrix[x - 1][y], matrix[x][y - 1], matrix[x + 1][y]]
    elif (x, y) == (len(matrix) - 1, 0):
        return [matrix[x - 1][y], matrix[x][y + 1]]
    elif x == len(matrix) - 1:
        return [matrix[x - 1][y], matrix[x][y - 1], matrix[x][y + 1]]
    elif x == 0:
        return [matrix[x][y - 1], matrix[x + 1][y], matrix[x][y + 1]]
    elif y == 0:
        return [matrix[x - 1][y], matrix[x + 1][y], matrix[x][y + 1]]

    return [matrix[x - 1][y], matrix[x][y - 1], matrix[x + 1][y], matrix[x][y + 1]]


def check_basin(matrix: field, x: int, y: int, visited_nodes: visited_type, r_len: int, c_len: int):
    if x < 0 or y < 0 or x > r_len or y > c_len or matrix[x][y] == 9 or (x, y) in visited_nodes:
        return

    visited_nodes.append((x, y))

    check_basin(matrix, x, y + 1, visited_nodes, r_len, c_len)
    check_basin(matrix, x, y - 1, visited_nodes, r_len, c_len)
    check_basin(matrix, x - 1, y, visited_nodes, r_len, c_len)
    check_basin(matrix, x + 1, y, visited_nodes, r_len, c_len)


heights_sum: list[tuple[int, int, int]] = []
for i in range(len(field)):
    for j in range(len(field[0])):
        cur = field[i][j]
        window = extract_window(i, j, field)
        if cur < min(window):
            heights_sum.append((i, j, cur))

print(sum(value + 1 for _, _, value in heights_sum))

basins = []
for heights in heights_sum:
    i, j, z = heights
    visited: list[tuple[int, int]] = []
    check_basin(field, i, j, visited, len(field) - 1, len(field[0]) - 1)
    basins.append(len(visited))

basins.sort(reverse=True)
print(basins[0] * basins[1] * basins[2])