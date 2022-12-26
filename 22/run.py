#!/usr/bin/env python3

from re import findall
from collections import defaultdict
from sys import stdin

#
# PARSING
#

parts = stdin.read().split('\n\n')

grid = defaultdict(lambda: ' ',
                   {(x, y): c
                    for y, row in enumerate(parts[0].split('\n'))
                    for x, c in enumerate(row)})

instructions = [int(c) if c.isdigit() else c
                for c in findall(r'\d+|[RL]', parts[1])]

#
# PART 1
#


def follow(grid, instructions, cube=False):
    x = min(x for x, y in grid if y == 0 and grid[x, y] == '.')
    position = (x, 0, 0)
    for instruction in instructions:
        position = move(grid, position, instruction, cube)

    x, y, r = position
    return (y + 1) * 1000 + (x + 1) * 4 + r


def move(grid, position, instruction, cube):
    x, y, r = position
    if type(instruction) is int:
        for _ in range(instruction):
            dx, dy = [(1, 0), (0, 1), (-1, 0), (0, -1)][r]
            c = grid[x + dx, y + dy]
            if c == '.':
                x += dx
                y += dy
            elif c == '#':
                break
            else:
                dst = wrap(grid, x, y, r, cube)
                if grid[dst[:2]] == '#':
                    break
                x, y, r = dst
    else:
        r = (r + (1 if instruction == 'R' else -1)) % 4
    return x, y, r


def wrap(grid, x, y, r, cube):
    if cube:
        return wrap_cube_simple(grid, x, y, r)
    if r == 0:
        x = min(xx for xx, yy in grid if yy == y and grid[xx, yy] != ' ')
    elif r == 1:
        y = min(yy for xx, yy in grid if xx == x and grid[xx, yy] != ' ')
    elif r == 2:
        x = max(xx for xx, yy in grid if yy == y and grid[xx, yy] != ' ')
    elif r == 3:
        y = max(yy for xx, yy in grid if xx == x and grid[xx, yy] != ' ')
    return x, y, r


#
# PART 2
#

lines = parts[0].split('\n')
rows = len(lines)
cols = len(lines[0])

pattern = set((x, y)
              for x in range(cols // 50)
              for y in range(rows // 50)
              if grid[x * 50, y * 50] != ' ')

# My input's pattern:
#
#     12
#     3
#    45
#    6
assert pattern == {(1, 2), (1, 1), (0, 3), (2, 0), (0, 2), (1, 0)}


def wrap_cube_simple(grid, x, y, r):
    # Face 1
    if x == 50 and 0 <= y and y < 50 and r == 2:
        return 0, 149 - y % 50, 0
    if 50 <= x and x < 100 and y == 0 and r == 3:
        return 0, 150 + x % 50, 0

    # Face 2
    if x == 149 and 0 <= y and y < 50 and r == 0:
        return 99, 149 - y % 50, 2
    if 100 <= x and x < 150 and y == 49 and r == 1:
        return 99, 50 + x % 50, 2
    if 100 <= x and x < 150 and y == 0 and r == 3:
        return 0 + x % 50, 199, 3

    # Face 3
    if x == 99 and 50 <= y and y < 100 and r == 0:
        return 100 + y % 50, 49, 3
    if x == 50 and 50 <= y and y < 100 and r == 2:
        return 0 + y % 50, 100, 1

    # Face 4
    if 0 <= x and x < 50 and y == 100 and r == 3:
        return 50, 50 + x % 50, 0
    if x == 0 and 100 <= y and y < 150 and r == 2:
        return 50, 49 - y % 50, 0

    # Face 5
    if x == 99 and 100 <= y and y < 150 and r == 0:
        return 149, 49 - y % 50, 2
    if 50 <= x and x < 100 and y == 149 and r == 1:
        return 49, 150 + x % 50, 2

    # Face 6
    if x == 49 and 150 <= y and y < 200 and r == 0:
        return 50 + y % 50, 149, 3
    if 0 <= x and x < 50 and y == 199 and r == 1:
        return 100 + x % 50, 0, 1
    if x == 0 and 150 <= y and y < 200 and r == 2:
        return 50 + y % 50, 0, 1

    raise Exception('Could not find adequate wrap', (x, y, r))


print(follow(grid, instructions))
print(follow(grid, instructions, cube=True))
