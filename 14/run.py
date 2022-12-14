#!/usr/bin/env python3

from collections import defaultdict
from sys import stdin
from itertools import product


def load(f):
    def _range(a, b):
        if a > b:
            a, b = b, a
        return range(a, b + 1)

    grid = defaultdict(lambda: '.')
    for line in stdin:
        points = [tuple(map(int, p.split(','))) for p in line.split(' -> ')]
        for segment in zip(points, points[1:]):
            for x, y in product(*map(_range, *segment)):
                grid[x, y] = '#'

    return grid


def count_drops(grid, floor=False):
    g = grid.copy()
    maxx = max(x for (x, y) in g)
    maxy = max(y for (x, y) in g)
    i = 0
    while drop(g, maxx, maxy, floor):
        i += 1
    if floor:
        i += 1
    return i


def drop(grid, maxx, maxy, floor):
    sx, sy = 500, 0
    while True:
        if not floor:
            if sx > maxx or sy > maxy:
                return False
        if sy != maxy + 1:
            if grid[sx, sy + 1] == '.':
                sy += 1
                continue
            if grid[sx - 1, sy + 1] == '.':
                sx -= 1
                sy += 1
                continue
            if grid[sx + 1, sy + 1] == '.':
                sx += 1
                sy += 1
                continue
        grid[sx, sy] = 'o'
        return (sx, sy) != (500, 0)


grid = load(stdin)
print(count_drops(grid))
print(count_drops(grid, floor=True))
