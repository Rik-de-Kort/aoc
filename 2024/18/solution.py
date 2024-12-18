import math
from collections import defaultdict
from pathlib import Path

folder = Path(__file__).parent


def parse_coords(x, y):
    return y + x * 1j


with open(folder / 'input.txt') as handle:
    data = [parse_coords(*(int(x.strip()) for x in line.split(','))) for line in handle.readlines() if line.strip()]

x_min, x_max = 0, 71
y_min, y_max = 0, 71
# x_min, x_max = 0, 7
# y_min, y_max = 0, 7


def in_bounds(z):
    return x_min <= z.real < x_max and y_min <= z.imag < y_max


def neighbours(z, blocks):
    return [
        z + direction for direction in [1, -1, 1j, -1j]
        if z + direction not in blocks and in_bounds(z + direction)
    ]


def display(blocks, start, target, route):
    print('\n'.join(
        ''.join(
            '#' if i + j * 1j in blocks else 'S' if i + j * 1j == start else 'E' if i + j * 1j == target else 'O' if i + j * 1j in route else '.'
            for j in range(y_min, y_max)
        )
        for i in range(x_min, x_max)
    ))



def min_path(blocks, start, target) -> int:
    done = {start}
    unvisited = set()
    frontier = set(neighbours(start, blocks))
    d = defaultdict(lambda: (math.inf, []))
    d[start] = (0, [start])
    for z in frontier:
        d[z] = (1, [start, z])

    while frontier:
        if all(math.isinf(d[z][0]) for z in frontier): raise ValueError
        z = min(frontier, key=lambda z: d[z][0])
        frontier.remove(z)
        done.add(z)
        z_len, z_route = d[z]
        for w in neighbours(z, blocks):
            if w in done: continue
            w_len, w_route = d[w]
            if z_len + 1 < w_len:
                d[w] = (z_len + 1, z_route + [w])
            frontier.add(w)
    return d[target][0]

print(min_path(set(data[:1024]), 0+0j, 70+70j))
# print(min_path(set(data[:12]), 0+0j, 6+6j))

def is_blocked(blocks, start, target) -> bool:
    return math.isinf(min_path(blocks, start, target))

lo, hi = 0, len(data)
while abs(lo - hi) > 1:
    pivot = (hi + lo) // 2
    if is_blocked(set(data[:pivot]), 0+0j, 70+70j):
    # if is_blocked(set(data[:pivot]), 0+0j, 6+6j):
        hi = pivot
    else:
        lo = pivot

# print(lo, is_blocked(set(data[:lo]), 0+0j, 6+6j))
# print(hi, is_blocked(set(data[:hi]), 0+0j, 6+6j))
print(lo, is_blocked(set(data[:lo]), 0+0j, 70+70j))
print(hi, is_blocked(set(data[:hi]), 0+0j, 70+70j))
print(f'{int(data[hi-1].imag)},{int(data[hi-1].real)}')
