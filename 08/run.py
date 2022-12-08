#!/usr/bin/env python3

from functools import reduce
from operator import mul
from sys import stdin

grid = {}
for y, line in enumerate(stdin):
    for x, c in enumerate(line.rstrip()):
        grid[x, y] = c
W, H = x + 1, y + 1


def is_visible(x, y):
    height = grid[x, y]
    return (
        x in [0, W - 1] or y in [0, H - 1]
        or any(height > max(grid[pos] for pos in v) for v in views(x, y)))


def score(x, y):
    h = grid[x, y]
    return reduce(mul, (visible_trees(h, v) for v in views(x, y)))


def visible_trees(height, trees):
    return sum(1 for _ in takewhile_(lambda pos: grid[pos] < height, trees))


def views(x, y):
    '''Yields one line of sight for each direction starting from (x, y)'''
    yield ((x, yy) for yy in range(y - 1, -1, -1))
    yield ((xx, y) for xx in range(x - 1, -1, -1))
    yield ((xx, y) for xx in range(x + 1, W))
    yield ((x, yy) for yy in range(y + 1, H))


def takewhile_(predicate, iterable):
    '''Like itertools.takewhile, but inclusive of the edge'''
    for x in iterable:
        yield x
        if not predicate(x):
            break


print(sum(1 for x, y in grid if is_visible(x, y)))
print(max(score(x, y) for x, y in grid))
