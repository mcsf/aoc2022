#!/usr/bin/env python3

from itertools import tee
from sys import stdin


def flatten(file):
    for line in file:
        yield 0
        if 'addx' in line:
            yield int(line.split()[1])


def run(signal):
    x = 1
    for t, val in enumerate(signal, start=1):
        yield t, x
        x += val


def strength(signal):
    return sum(t * x for t, x in signal if t % 40 == 20)


def draw(signal):
    pixels = ['.' for _ in range(40 * 6)]
    for t, x in signal:
        if abs((t - 1) % 40 - x) <= 1:
            pixels[t - 1] = '#'
    return '\n'.join(
            ''.join(pixels[(40 * i):(40 * (i + 1))])
            for i in range(6))


signal = run(flatten(stdin))
for part, signal in zip((strength, draw), tee(signal)):
    print(part(signal))
