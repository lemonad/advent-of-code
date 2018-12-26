"""
Advent of Code Graph helper (Jonas Nockert / @lemonad)

"""
from collections import deque
from enum import Enum, unique
import heapq

import numpy as np


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


class GridGraph:
    def __init__(self):
        self.next_index = 1
        self.g = {}

    @classmethod
    def from_chararray(cls, m, skip_symbol="#"):
        def coord_to_index(y, x, n_rows, m_cols):
            if x < 0 or x >= m_cols or y < 0 or y >= m_rows:
                return None
            return y * m_cols + x

        graph = cls()

        n_rows, m_cols = np.shape(m)
        for n in range(n_rows):
            for m in range(m_cols):
                symbol = m[n, m].decode("utf-8")
                if symbol == skip_symbol:
                    continue
                i = coord_to_index(n, m, n_rows, m_cols)
                graph.add_node(
                    i, extra={"symbol": symbol, "pos": (m, n)}  # Note: (x, y).
                )
                # east = coord_to_index(n, m + 1, n_rows, m_cols)
                # south = coord_to_index(n + 1, m, n_rows, m_cols)
                north = coord_to_index(n - 1, m, n_rows, m_cols)
                if north:
                    graph.add_edge(i, north)
                west = coord_to_index(n, m - 1, n_rows, m_cols)
                if west:
                    graph.add_edge(i, west)
        return graph

    def print(self):
        print(self.g)

    def get_node(self, node_id):
        if node_id not in self.g:
            return None
        return self.g[node_id]

    def add_node(self, node_id=None, extra=None):
        if node_id is None:
            node_id = max(self.g.keys()) + 1
        self.g[node_id] = {"adj": set(), "weights": {}}
        if extra:
            self.g[node_id].update(extra)
        return node_id

    def add_edge(self, src_node_id, dest_node_id, directed=False, weight=1):
        self.g[src_node_id]["adj"].add(dest_node_id)
        self.g[src_node_id]["weights"][dest_node_id] = weight
        if not directed:
            self.g[dest_node_id]["adj"].add(src_node_id)
            self.g[dest_node_id]["weights"][src_node_id] = weight

    def dims(self):
        min_x = 0
        max_x = 0
        min_y = 0
        max_y = 0
        for k in self.g.keys():
            min_x = min(min_x, self.g[k]["pos"][0])
            max_x = max(max_x, self.g[k]["pos"][0])
            min_y = min(min_y, self.g[k]["pos"][1])
            max_y = max(max_y, self.g[k]["pos"][1])
        return (min_x, max_x, min_y, max_y)

    def all_shortest_paths(self, source_node_id):
        for node_id in sorted(self.g.keys(), reverse=True):
            if node_id == source_node_id:
                continue
            pathlen = self.shortest_path(source_node_id, node_id)
            yield pathlen

    def shortest_path(self, start, goal):
        if "dist" in self.g[goal]:
            return self.g[goal]["dist"]

        frontier = PriorityQueue()
        frontier.put(start, 0)
        cost_so_far = {}
        cost_so_far[start] = 0

        while not frontier.empty():
            current = frontier.get()

            if (
                "dist" in self.g[current]
                and cost_so_far[current] != self.g[current]["dist"]
            ):
                raise Exception("What!")
            self.g[current]["dist"] = cost_so_far[current]

            if current == goal:
                break

            for next in self.g[current]["adj"]:
                new_cost = cost_so_far[current] + self.g[current]["weights"][next]
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost
                    frontier.put(next, priority)

        return cost_so_far[goal]
