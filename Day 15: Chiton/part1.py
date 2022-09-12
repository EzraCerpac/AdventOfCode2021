from queue import PriorityQueue
from typing import Tuple

import numpy as np


def part1():
    graph = Graph()
    print(dijkstra(graph))


def part2():
    graph = Graph(multiply=5)
    print(dijkstra(graph))


class Graph:
    def __init__(self, matrix_dir: str = 'input.txt', multiply: int = 0):
        self.matrix = np.array([[int(risk)
                                 for risk in line.strip()]
                                for line in open(matrix_dir).readlines()])
        if multiply:
            self.multiply_matrix(multiply)
        self.v, self.h = self.matrix.shape
        self.edges = self.matrix
        self.visited = set()

    @staticmethod
    def _translate_risk(risk, x, y, tile_width, tile_height):
        x_translation = x // tile_width
        y_translation = y // tile_height

        risk_translation = (risk + x_translation + y_translation - 1) % 9 + 1

        return risk_translation

    def multiply_matrix(self, n: int) -> None:
        tile_width = self.matrix.shape[0]
        full_width = tile_width * n
        tile_height = self.matrix.shape[1]
        full_height = tile_height * n

        self.matrix = np.array([[
            self._translate_risk(self.matrix[y % tile_height, x % tile_width], x, y, tile_width, tile_height)
            for x in range(full_width)] for y in range(full_height)
        ])


def dijkstra(graph: Graph, start_vertex: Tuple[int, int] = (0, 0)):
    D = {(v, h): float('inf') for v in range(graph.v) for h in range(graph.h)}
    D[start_vertex] = 0

    pq = PriorityQueue()
    pq.put((0, start_vertex))

    while not pq.empty():
        (dist, current_vertex) = pq.get()
        graph.visited.add(current_vertex)

        for neighbor in [(current_vertex[0]-1, current_vertex[1]), (current_vertex[0]+1, current_vertex[1]),
                         (current_vertex[0], current_vertex[1]-1), (current_vertex[0], current_vertex[1]+1)]:
            if neighbor in graph.visited or neighbor not in D:
                continue
            old_cost = D[neighbor]
            new_cost = D[current_vertex] + graph.edges[neighbor]
            if new_cost < old_cost:
                pq.put((new_cost, neighbor))
                D[neighbor] = new_cost
    return D[(graph.v - 1, graph.h - 1)]


if __name__ == '__main__':
    part2()
