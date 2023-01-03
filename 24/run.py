#!/usr/bin/env python3

from collections import namedtuple
from functools import cache
from heapq import heappush, heappop
from sys import maxsize, stdin

lines = stdin.readlines()

# Width and height
W = len(lines[0].strip()) - 2
H = len(lines) - 2

# Start and end positions
S = (lines[0].index('.') - 1, -1)
E = (lines[-1].index('.') - 1, H)

# Blizzards as cacheable set of positions
R = ['>', 'v', '<', '^']
BLIZZARDS = frozenset({(x - 1, y - 1, R.index(c))
                       for y, row in enumerate(lines)
                       for x, c in enumerate(row)
                       if c in R})


class Blizzards:
    @staticmethod
    @cache
    def positions(t) -> frozenset[tuple[int, int]]:
        return frozenset((x, y) for (x, y, _) in Blizzards._get_iter(t))

    @staticmethod
    @cache
    def _get_iter(t):
        return Blizzards._move(Blizzards._get_iter(t - 1)) if t else BLIZZARDS

    @staticmethod
    def _move(blizzards):
        dxy = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        return frozenset(((x + (d := dxy[r])[0]) % W, (y + d[1]) % H, r)
                         for x, y, r in blizzards)


class Player:
    @staticmethod
    def positions(position, goal):
        x, y = position
        if position in (S, E):
            yield (x, 0 if y == -1 else E[1] - 1)  # Move out of initial slot
            yield position
        elif mh(position, goal) == 1:  # Move into goal
            yield goal
        else:
            for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
                xx = x + dx
                yy = y + dy
                if xx >= 0 and xx < W and yy >= 0 and yy < H:
                    yield xx, yy  # Move in all possible directions


class Search:
    State = namedtuple('State', 'h, t, position')

    @staticmethod
    def run(start, end, t_init):
        queue = []
        seen = set()
        best = maxsize
        init = Search.State(mh(start, end) + t_init, t_init, start)
        heappush(queue, init)

        while queue:
            entry = heappop(queue)
            h, t, position = entry

            if h > best or entry in seen:
                continue

            seen.add(entry)

            if position == end and t < best:
                best = t

            bs = Blizzards.positions(t + 1)
            for p in Player.positions(position, end):
                if p not in bs:
                    state = Search.State(t + mh(p, end), t + 1, p)
                    if state not in seen:
                        heappush(queue, state)

        return best


def mh(a, b):
    '''Manhattan distance between two points'''
    return sum(abs(ax - bx) for ax, bx in zip(a, b))


print(t := Search.run(S, E, 0))
t = Search.run(E, S, t)
print(t := Search.run(S, E, t))
