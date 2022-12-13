#!/usr/bin/env python3

import curses
import time
import fileinput
import heapq
import math

from bisect import bisect
from collections import defaultdict


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

    # Bonus
    prevs = {}

    # Run Dijkstra's algorithm
    queue = Heap(startset)
    while queue:
        curr = queue.pop()
        if curr == end:
            return D[curr], prevs
        for e, d in G[curr].items():
            dist = D[curr] + d
            if dist < D[e]:
                D[e] = dist
                prevs[e] = curr
                queue.push(e)


# Bonus!
def draw_solution(stdscr, reverse=False):
    global prevs

    curr = end
    path = []
    while True:
        path.insert(0, curr)
        if curr == start or curr not in prevs:
            break
        curr = prevs[curr]

    if reverse:
        path.reverse()

    stdscr.clear()

    visited = set()
    for i, step in enumerate(path):
        for x, y in V:
            if (x, y) == step:
                c = '@'
            elif (x, y) in visited:
                c = '·'
            elif (x, y) == start:
                c = 'S'
            elif (x, y) == end:
                c = 'E'
            else:
                c = chr(V[x, y] + ord('a'))
            stdscr.addstr(y, x, c)
        visited.add(step)
        stdscr.addstr(y + 2, 0, f'{step} [distance: {i}]')
        stdscr.refresh()
        time.sleep(0.001)
    stdscr.addstr(y + 3, 0, 'Ta-dah!')
    stdscr.getkey()


with fileinput.input() as f:
    G, V, start, end = build_graph(f)

try:
    distance1, prevs = dijkstra(G, [start], end)
    curses.wrapper(draw_solution)

    startset = [(x, y) for (x, y), height in V.items() if height == 0]
    distance2, prevs = dijkstra(G, startset, end)
    curses.wrapper(draw_solution, reverse=True)
except curses.error:
    print('Could not render. Is your terminal interactive and large enough?')

print(distance1)
print(distance2)
