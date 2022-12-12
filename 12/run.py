#!/usr/bin/env python3

import heapq
import math

from bisect import bisect
from collections import defaultdict
from sys import stdin


def build_graph(file):
    def adjacent(x, y):
        ds = ((-1, 0), (1, 0), (0, -1), (0, 1))
        return ((x + dx, y + dy) for dx, dy in ds)

    V = {}  # V[x, y] = height
    for y, row in enumerate(file):
        for x, c in enumerate(row.strip()):
            if c == 'S':
                start = x, y
                c = 'a'
            elif c == 'E':
                end = x, y
                c = 'z'
            V[x, y] = ord(c) - ord('a')

    G = defaultdict(dict)  # G[x, y] = {(x', y'): distance}
    for (x, y), height in V.items():
        for edge in adjacent(x, y):
            if edge in V and V[edge] - height <= 1:
                G[x, y][edge] = 1

    return (G, V, start, end)


def dijkstra(G, startset, end):
    D = defaultdict(lambda: math.inf)  # (x, y) → shortest distance
    for x, y in startset:
        D[x, y] = 0

    # Priority queue that makes up for `heapq`'s shortcomings
    class Heap(list):
        def push(self, x):
            idx = bisect(self, x)
            found = len(self) > (idx - 1) >= 0 and self[idx - 1] == x
            if not found:
                heapq.heappush(queue, x)

        def pop(self):
            return heapq.heappop(self)

    # Run Dijkstra's algorithm
    queue = Heap(startset)
    while queue:
        curr = queue.pop()
        if curr == end:
            return D[curr]
        for e, d in G[curr].items():
            dist = D[curr] + d
            if dist < D[e]:
                D[e] = dist
                queue.push(e)


G, V, start, end = build_graph(stdin)
print(dijkstra(G, [start], end))

startset = [(x, y) for (x, y), height in V.items() if height == 0]
print(dijkstra(G, startset, end))
