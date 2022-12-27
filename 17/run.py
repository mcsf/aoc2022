#!/usr/bin/env python3

from sys import stdin


class Cycle:
    '''Replacement for itertools.cycle whose index is public'''
    def __init__(self, xs):
        self.xs = xs
        self.index = 0

    def __next__(self):
        x = self.xs[self.index]
        self.index = (self.index + 1) % len(self.xs)
        return x


# Jet pattern
J = Cycle([1 if c == '>' else - 1 for c in stdin.read().strip()])

# Rock pattern
r1 = ((0, 0), (1, 0), (2, 0), (3, 0))
r2 = ((1, 2), (0, 1), (1, 1), (2, 1), (1, 0))
r3 = ((2, 2), (2, 1), (0, 0), (1, 0), (2, 0))
r4 = ((0, 0), (0, 1), (0, 2), (0, 3))
r5 = ((0, 0), (1, 0), (0, 1), (1, 1))
R = Cycle([r1, r2, r3, r4, r5])

# Occupied space
S = {(x, -1) for x in range(7)}


def drop():
    r = next(R)
    x, y = 2, max(y for x, y in S) + 4

    while True:
        next_x = x + next(J)
        if all((xx := next_x + dx) >= 0 and xx <= 6 and (xx, y + dy) not in S
               for dx, dy in r):
            x = next_x
        next_y = y - 1
        if any((x + dx, next_y + dy) in S for dx, dy in r):
            break
        y = next_y

    for dx, dy in r:
        S.add((x + dx, y + dy))


def height():
    return 1 + max(y for x, y in S)


def snapshot():
    ymax = max(y for x, y in S)
    top = frozenset((x, ymax - y) for x, y in S if ymax - y <= 100)
    return (top, J.index, R.index)


seen = {}  # type: ignore
h = 0
t = 0
while t < 1000000000000:

    # Part 1
    if t == 2022:
        print(height())

    # Part 2
    if (s := snapshot()) in seen:
        curr = (t, height())
        dt, dh = (a - b for a, b in zip(curr, seen[s]))
        k = (1000000000000 - t) // dt
        t += dt * k
        h += dh * k
    else:
        seen[s] = (t, height())

    drop()
    t += 1

print(height() + h)
