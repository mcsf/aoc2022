#!/usr/bin/env python3

from functools import cmp_to_key
from json import loads
from math import prod
from sys import stdin


def cmp(a, b):
    if type(a) is type(b) is int:
        if a != b:
            return -1 if a < b else 1
        return 0

    if type(a) is int:
        a = [a]
    elif type(b) is int:
        b = [b]

    try:
        for aa, bb in zip(a, b, strict=True):
            order = cmp(aa, bb)
            if order:
                return order
    except ValueError:
        return -1 if len(a) < len(b) else 1

    return 0


raw = stdin.read()
pairs = [[loads(p) for p in pair.strip().split('\n')]
         for pair in raw.split('\n\n')]
print(sum(i for i, pair in enumerate(pairs, 1) if cmp(*pair) == -1))

dividers = [[[2]], [[6]]]
packets = [loads(p) for p in raw.strip().split('\n') if p]
packets += dividers
packets.sort(key=cmp_to_key(cmp))
print(prod(i for i, p in enumerate(packets, 1) if p in dividers))
