from functools import reduce as fold
from itertools import chain, repeat, combinations
from math import ceil, floor

def at_depth(pair, depth=4):
    if depth == 0:
        return () if isinstance(pair, (list, tuple)) else None
    elif isinstance(pair, int):
        return None

    x, y = pair
    if (result := at_depth(x, depth=depth-1)) is not None:
        return (0, *result)
    elif (result := at_depth(y , depth=depth-1)) is not None:
        return (1, *result)
    else:
        return None

def ge_10(pair):
    if isinstance(pair, int):
        return None if pair < 10 else ()
    
    x, y = pair
    if (result := ge_10(x)) is not None:
        return (0, *result)
    elif (result := ge_10(y)) is not None:
        return (1, *result)
    else:
        return None


def get(item, idx):
    result = item
    for i in idx:
        result = result[i]
    return result

def set_value(item, idx, value, repeat_val=1):
    to_set = item
    *idx, last = idx
    for i in idx: to_set = to_set[i]
    to_set[last] = value

def complete(item, idx, direction='left'):
    result = []
    sub = item
    for i in chain(idx, repeat(1 if direction == 'left' else 0)):
        if isinstance(get(item, result), int): return tuple(result)
        else: result.append(i)


def reduce(item):
    while True:
        if (idx := at_depth(item, 4)) is not None:
            left, right = get(item, idx)
            if not all(i == 0 for i in idx):  # Not exploding leftmost item
                i_left = idx[::-1].index(1) + 1
                idx_left = complete(item, idx[:-i_left] + (0,), direction='left')
                set_value(item, idx_left, get(item, idx_left) + left)
            if not all(i == 1 for i in idx):  # Not exploding rightmost item
                i_right = idx[::-1].index(0) + 1
                idx_right = complete(item, idx[:-i_right] + (1,), direction='right')
                set_value(item, idx_right, get(item, idx_right) + right)
            set_value(item, idx, 0)
        elif (idx := ge_10(item)) is not None:
            val = get(item, idx)
            set_value(item, idx, [floor(val/2), ceil(val/2)])
        else:
            break
    return item

def add(a, b):
    return reduce([a, b])

def magnitude(item):
    if isinstance(item, int): return item
    left, right = item
    return 3*magnitude(left) + 2*magnitude(right)

from copy import deepcopy as copy

with open('input') as handle:
    data = [eval(line) for line in handle.readlines()]

print(max(magnitude(add(copy(first), copy(second))) for first in data for second in data))

with open('input') as handle:
    data = [eval(line) for line in handle.readlines()]
result, *data = data
result = fold(add, data, result)
print(magnitude(result))





















