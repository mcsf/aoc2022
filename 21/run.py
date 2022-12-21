#!/usr/bin/env python3

from sys import stdin
from functools import cache
from operator import add, sub, mul, truediv

# https://github.com/karpathy/micrograd
# -> pip install micrograd
from micrograd.engine import Value  # type: ignore

monkeys = {}
for line in stdin:
    name, body = line.split(': ', 1)
    monkeys[name] = int(body) if body[0].isdigit() else body.split()

OPS = {'+': add, '-': sub, '*': mul, '/': truediv}


@cache
def build_value(name):
    m = monkeys[name]
    if type(m) is int:
        return Value(m)
    a, op, b = m
    return OPS[op](build_value(a), build_value(b))


# Part 1
values = {key: build_value(key) for key in monkeys}
print(int(values['root'].data))


# Part 2
def solve_humn():
    a, _, b = monkeys['root']

    # At least one of the two values `a` and `b` that `root` depends on must
    # depend on `humn`. Backpropagation is cheap here, so just use the first
    # value with a non-zero grad.
    for i, target in enumerate((a, b)):
        # Reset
        for v in values.values():
            v.grad = 0
        values[a].backward()
        if values['humn'].grad:
            break

    # Difference between `a` and `b`. Its sign must be flipped depending on
    # which value we are solving for.
    diff = values['root'].data
    if i == 0:
        diff = -diff

    # Determine how much to increment the value of `humn` in order to increment
    # `target` by `diff. Finally, return the value that `humn` must have.
    needs = diff / values['humn'].grad
    return int(values['humn'].data + needs)


# Replacing the operation of `root` with `-` allows us to quantity the effects
# of `humn` on `root` by solving for `a - b == 0`.
monkeys['root'][1] = '-'  # type: ignore
build_value.cache_clear()
values = {key: build_value(key) for key in monkeys}
print(solve_humn())
