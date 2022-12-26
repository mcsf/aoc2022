#!/usr/bin/python3

import math

from collections import namedtuple
from functools import reduce
from itertools import product
from re import findall
from sys import stdin

Sensor = namedtuple('Sensor', 'x, y, r')
Beacon = namedtuple('Beacon', 'x, y')
Segment = namedtuple('Segment', 'a, b')

sensors = []
beacons = set()

for line in stdin:
    sx, sy, bx, by = map(int, findall(r'-?\d+', line))
    r = abs(sx - bx) + abs(sy - by)
    sensors.append(Sensor(sx, sy, r))
    beacons.add(Beacon(bx, by))


def x_segments(row: int) -> list[Segment]:
    result = []
    beacon_xs = {x for x, y in beacons if y == row}
    for (x, y, r) in sensors:
        dx = r - abs(row - y)
        if dx >= 0:
            if beacon_xs:
                for bx in beacon_xs:  # FIXME
                    if x - dx <= bx and bx <= x + dx:
                        result.append(Segment(x - dx, bx - 1))
                        result.append(Segment(bx + 1, x + dx))
                    else:
                        result.append(Segment(x - dx, x + dx))
            else:
                result.append(Segment(x - dx, x + dx))
    result.sort()
    return result


def y_segments(col: int) -> list[Segment]:
    result = []
    beacon_ys = {y for x, y in beacons if x == col}
    for (x, y, r) in sensors:
        dy = r - abs(col - x)
        if dy >= 0:
            if beacon_ys:
                for by in beacon_ys:  # FIXME
                    if y - dy <= by and by <= y + dy:
                        result.append(Segment(y - dy, by - 1))
                        result.append(Segment(by + 1, y + dy))
                    else:
                        result.append(Segment(y - dy, y + dy))
            else:
                result.append(Segment(y - dy, y + dy))
    result.sort()
    return result


def condense(ss: list[Segment]) -> list[Segment]:
    def aux(acc: list[Segment], s2: Segment):
        if not acc:
            return [s2]
        s1 = acc[-1]
        if s2.b < s2.a:
            return acc
        elif s2.a <= s1.b:
            acc[-1] = Segment(min(s1.a, s2.a), max(s1.b, s2.b))
        else:
            acc.append(s2)
        return acc
    return reduce(aux, ss, [])


def measure(ss: list[Segment]) -> int:
    L = 0
    prev = -math.inf
    for (a, b) in ss:
        if a < prev + 1:
            a = max(prev + 1, a + 1)
        L += max(0, b - a + 1)
        prev = max(prev, b)
    return L


def invert(ss: list[Segment], smin: int, smax: int) -> list[Segment]:
    result = []

    if not ss:
        return [Segment(smin, smax)]

    if ss[0].a - smin > 0:
        result.append(Segment(smin, ss[0].a - 1))

    for s1, s2 in zip(ss, ss[1:]):
        if s1.b < s2.a + 1:
            result.append(Segment(s1.b + 1, s2.a - 1))

    if smax - ss[-1].b > 0:
        result.append(Segment(ss[-1].b + 1, smax))

    return result


def points(ss: list[Segment]) -> set[int]:
    return {p for a, b in ss for p in range(a, b + 1)}


def intersect(y_gaps: list[Segment], x_gaps: list[Segment]):
    # Assume condensed
    return set(product(points(y_gaps), points(x_gaps)))


def tuning_frequency(size):
    for y in range(size + 1):
        x_gaps = points(invert(condense(x_segments(y)), 0, size))
        for x in x_gaps:
            y_gaps = points(invert(condense(y_segments(x)), 0, size))
            if y in y_gaps and (x, y) not in beacons:
                return x * 4000000 + y


is_sample = sensors[0] == Sensor(x=2, y=18, r=7)
print(measure(condense(x_segments(10 if is_sample else 2000000))))
print(tuning_frequency(20 if is_sample else 4000000))
