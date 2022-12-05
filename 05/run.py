#!/usr/bin/env python3

import re
import sys

N = 9
stacks9000 = [[] for _ in range(N)]  # type: list[list[str]]
stacks9001 = [[] for _ in range(N)]  # type: list[list[str]]

for line in sys.stdin:
    if '[' in line:
        for m in re.finditer(r'[A-Z]+', line):
            crate = m.group()
            stack = ((m.start() + 3) // 4) - 1
            stacks9000[stack].insert(0, crate)
            stacks9001[stack].insert(0, crate)
    elif 'move' in line:
        n, src, dst = map(int, re.findall(r'[0-9]+', line))
        dstIdx = len(stacks9001[dst-1])
        for _ in range(n):
            stacks9000[dst-1].append(stacks9000[src-1].pop())
            stacks9001[dst-1].insert(dstIdx, stacks9001[src-1].pop())

print(''.join(s[-1] for s in stacks9000))
print(''.join(s[-1] for s in stacks9001))
