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
    coord = 0 if motion in ['R', 'L'] else 1
    knot[coord] += 1 if motion in ['R', 'U'] else -1


def follow(knots):
    for prev, knot in zip(knots, knots[1:]):
        if not all(abs(a - b) <= 1 for a, b in zip(knot, prev)):
            knot[0] += signum(prev[0] - knot[0])
            knot[1] += signum(prev[1] - knot[1])


def signum(n):
    return 1 if n > 0 else -1 if n < 0 else 0


print(simulate([[0, 0] for _ in range(2)]))
print(simulate([[0, 0] for _ in range(10)]))
