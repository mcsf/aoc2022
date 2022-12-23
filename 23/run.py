#!/usr/bin/env python3

from collections import Counter
from itertools import count, product
from sys import stdin

elves = {(x, y)
         for y, row in enumerate(stdin)
         for x, c in enumerate(row.strip())
         if c == '#'}

directions = ['N', 'S', 'W', 'E']


def round():
    if result := decide():
        proposals, direction = result
        move(proposals)
        rotate(direction)
        return True


def decide():
    proposals = {}
    considered = set()

    for e in elves:
        if any(a in elves for a in adjacent(e)):
            for d in directions:
                if not any(a in elves for a in quadrant(e, d)):
                    considered.add(d)
                    proposals[e] = next(quadrant(e, d))
                    break

    if proposals:
        direction = next(d for d in directions if d in considered)
        return proposals, direction


def move(proposals):
    counts = Counter(proposals.values())
    for e in proposals:
        if counts[proposals[e]] == 1:
            elves.remove(e)
            elves.add(proposals[e])


def rotate(direction):
    directions.remove(direction)
    directions.append(direction)


def adjacent(xy):
    x, y = xy
    for dx, dy in product((-1, 0, 1), repeat=2):
        if (dx, dy) != (0, 0):
            yield (x + dx, y + dy)


quadrants = {
    'N': ((0, -1), (1, -1), (-1, -1)),
    'S': ((0, 1), (1, 1), (-1, 1)),
    'W': ((-1, 0), (-1, -1), (-1, 1)),
    'E': ((1, 0), (1, -1), (1, 1)),
}


def quadrant(xy, q):
    x, y = xy
    for dx, dy in quadrants[q]:
        yield x + dx, y + dy


for t in count(1):
    if not round():
        print(t)
        break
    if t == 10:
        x1 = min(x for x, y in elves)
        x2 = max(x for x, y in elves)
        y1 = min(y for x, y in elves)
        y2 = max(y for x, y in elves)
        print(sum(1
                  for x in range(x1, x2 + 1)
                  for y in range(y1, y2 + 1)
                  if (x, y) not in elves))


# def draw(minx, maxx, miny, maxy):
#     for y in range(miny, maxy + 1):
#         for x in range(minx, maxx + 1):
#             print('#' if (x, y) in elves else '.', end='')
#         print()
