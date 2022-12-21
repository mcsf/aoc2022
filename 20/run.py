#!/usr/bin/env python3

from collections import deque
from sys import stdin

# Numbers aren't unique, so keep uniquely enumerated tuples instead
ns = [(int(n), _id) for _id, n in enumerate(stdin)]

# Capture the zero tuple to later call `xs.index(zero)`
zero = next(x for x in ns if x[0] == 0)


def mix(xs, count=1):
    seq = xs.copy()
    for _ in range(count):
        for x in seq:
            move(xs, x)
    return sum(nth(xs, n)[0] for n in (1000, 2000, 3000))


def move(xs, x: tuple[int, int]):
    n, _ = x

    # Align at x
    idx = xs.index(x)
    xs.rotate(-idx)

    # Move x by n positions
    xs.popleft()
    xs.rotate(-n % len(xs))
    xs.appendleft(x)


def nth(xs, n):
    idx = xs.index(zero)
    return xs[(idx + n) % len(xs)]


print(mix(deque(ns)))
print(mix(deque((n * 811589153, _id) for n, _id in ns), count=10))
