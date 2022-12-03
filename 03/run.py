#!/usr/bin/env python3

from sys import stdin
from functools import reduce
from operator import __and__


def priority(c):
    if c.isupper():
        return ord(c) - ord('A') + 27
    return ord(c) - ord('a') + 1


def split_half(line):
    half = len(line) // 2
    return (line[:half], line[half:])


def threes(xs):
    for i in range(0, len(xs), 3):
        yield xs[i:i+3]


def intersect(xs):
    return reduce(__and__, map(set, xs)).pop()


lines = [line.rstrip() for line in stdin]
print(sum(map(priority, map(intersect, map(split_half, lines)))))
print(sum(map(priority, map(intersect, threes(lines)))))
