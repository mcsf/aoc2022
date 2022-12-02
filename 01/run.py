#!/usr/bin/env python3

from sys import stdin

paragraphs = [p.strip().split('\n') for p in stdin.read().split('\n\n')]
elves = ([int(x) for x in p] for p in paragraphs)
sums = sorted((sum(e) for e in elves), reverse=True)

print(sums[0])
print(sum(sums[:3]))
