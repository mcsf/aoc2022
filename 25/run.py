#!/usr/bin/env python3

from sys import stdin

snafus = [line.strip() for line in stdin]


def decode(s: str) -> int:
    digits = {'2': 2, '1': 1, '0': 0, '-': -1, '=': -2}
    return sum(5**i * digits[c] for i, c in enumerate(reversed(s)))


def encode(d: int) -> str:
    s = ''
    while d:
        digit = d % 5
        s = str(digit) + s
        d //= 5
        if digit > 2:
            d += 1
    return s.replace('4', '-').replace('3', '=')


print(encode(sum(decode(s) for s in snafus)))
