#!/usr/bin/env python3

from sys import stdin
lines = (line.rstrip().split() for line in stdin)

# Normalize to (a, b), a ∈ [0,2], b ∈ [0,2]
rounds = [(ord(a) - ord('A'), ord(b) - ord('X')) for a, b in lines]


# Part 1
def score(a, b):
    outcome = 0
    diff = b - a
    if diff == 1 or diff == -2:
        outcome = 2
    elif diff == 0:
        outcome = 1
    return b + 1 + outcome * 3


print(sum(score(*r) for r in rounds))


# Part 2
def score(a, outcome):
    b = a
    if outcome == 2:
        b = (a + 1) % 3
    elif outcome == 0:
        b = (a - 1) % 3
    return b + 1 + outcome * 3


print(sum(score(*r) for r in rounds))
