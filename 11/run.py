#!/usr/bin/env python3

from collections import namedtuple
from functools import reduce
from heapq import nlargest
from math import lcm, prod
from re import findall
from sys import stdin


def parse_monkey(s):
    def ints(xs): return tuple(map(int, xs))
    def op(expr): return eval(f'lambda old: {expr}', {}, {})
    def dst(a, b, c): return lambda x: b if x % a == 0 else c
    xs = findall(r'(\w+ [+*] \w+|\d+)', s)[1:]
    return Monkey(ints(xs[:-4]), op(xs[-4]), int(xs[-3]), dst(*ints(xs[-3:])))


def play(n, worry_fn):
    items = [list(m.items) for m in monkeys]
    counts = [0 for _ in monkeys]
    for _ in range(n):
        for i, m in enumerate(monkeys):
            while items[i]:
                counts[i] += 1
                item = worry_fn(m.op(items[i].pop(0)))
                items[m.dst(item)].append(item)
    return prod(nlargest(2, counts))


Monkey = namedtuple('Monkey', ['items', 'op', 'div', 'dst'])
monkeys = [parse_monkey(s) for s in stdin.read().split('\n\n')]
base = reduce(lcm, [m.div for m in monkeys])
print(play(20, lambda x: x // 3))
print(play(10000, lambda x: x % base))
