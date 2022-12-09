#!/usr/bin/env python3

from sys import stdin

lines = (line.split() for line in stdin)
motions = [(motion, int(count)) for motion, count in lines]


def simulate(knots):
    visited = set()
    for motion, count in motions:
        for _ in range(count):
            move(knots[0], motion)
            follow(knots)
            visited.add(tuple(knots[-1]))
    return len(visited)


def move(knot, motion):
    if motion == 'R':
        knot[0] += 1
    elif motion == 'L':
        knot[0] -= 1
    elif motion == 'U':
        knot[1] += 1
    elif motion == 'D':
        knot[1] -= 1


def follow(knots):
    for prev, knot in zip(knots, knots[1:]):
        dist = sum(abs(ax - bx) for ax, bx in zip(knot, prev))
        if dist == 2 and prev[1] == knot[1]:
            knot[0] += 1 if prev[0] > knot[0] else -1
        elif dist == 2 and prev[0] == knot[0]:
            knot[1] += 1 if prev[1] > knot[1] else -1
        elif dist > 2:
            knot[0] += 1 if prev[0] > knot[0] else -1
            knot[1] += 1 if prev[1] > knot[1] else -1


print(simulate([[0, 0] for _ in range(2)]))
print(simulate([[0, 0] for _ in range(10)]))


# DEBUGGING
#
# from operator import itemgetter
# def print_state(label=''):
#     knots_with_origin = knots + [[0, 0]]
#     minx = min(map(itemgetter(0), knots_with_origin))
#     maxx = max(map(itemgetter(0), knots_with_origin))
#     miny = min(map(itemgetter(1), knots_with_origin))
#     maxy = max(map(itemgetter(1), knots_with_origin))
#     if maxx - minx < 5:
#         maxx += 5 - maxx + minx
#     if maxy - miny < 5:
#         maxy += 4 - maxy + miny
#     print(f'== {label} ==' if label else '')
#     for y in range(maxy, miny - 1, -1):
#         for x in range(minx, maxx + 1):
#             mark = 's' if [x, y] == [0, 0] else '.'
#             try:
#                 idx = next(i for i, k in enumerate(knots) if k == [x, y])
#                 mark = str(idx) if idx > 0 else 'H'
#             except StopIteration:
#                 pass
#             print(mark, end='')
#         print('')
#     print('')
