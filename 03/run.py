#!/usr/bin/env python3

from sys import stdin


def priority(c):
    if c.isupper():
        return ord(c) - ord('A') + 27
    return ord(c) - ord('a') + 1


def split_halfway(line):
    half = len(line) // 2
    return (line[:half], line[half:])


def threes(xs):
    for i in range(0, len(xs), 3):
        yield xs[i:i+3]


lines = [line.rstrip() for line in stdin]

rucksacks = (split_halfway(line) for line in lines)
common_items = [min(set(a) & set(b)) for a, b in rucksacks]
print(sum(priority(item) for item in common_items))

group_items = [min(set(a) & set(b) & set(c)) for a, b, c in threes(lines)]
print(sum(priority(item) for item in group_items))
