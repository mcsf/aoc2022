#!/usr/bin/env python3

import sys


def markerIndex(s, length):
    for i, s in enumerate(spans(s, length)):
        if len(set(s)) == length:
            return i + length


def spans(s, length):
    for i in range(0, len(s)):
        yield s[i:i+length]


for line in sys.stdin:
    print(markerIndex(line, 4))
    print(markerIndex(line, 14))
