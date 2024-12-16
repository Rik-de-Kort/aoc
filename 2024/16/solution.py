from collections import defaultdict
from enum import Enum
import math
from pathlib import Path

folder = Path(__file__).parent


class Direction(Enum):
    UP = -1
    DOWN = 1
    RIGHT = 1j
    LEFT = -1j


CW = {
    Direction.UP: Direction.RIGHT,
    Direction.RIGHT: Direction.DOWN,
    Direction.DOWN: Direction.LEFT,
    Direction.LEFT: Direction.UP,
}
CCW = {v: k for k, v in CW.items()}

with open(folder / 'input.txt') as handle:
    data = [[char for char in line.strip()] for line in handle.readlines() if line.strip()]
    direction = Direction.RIGHT
    maze = {}
    for i, line in enumerate(data):
        for j, c in enumerate(line):
            if c == 'S':
                start = i + j * 1j
                maze[i + j * 1j] = '.'
            elif c == 'E':
                end = i + j * 1j
                maze[i + j * 1j] = '.'
            else:
                maze[i + j * 1j] = c

i_min, i_max = 0, len(data)
j_min, j_max = 0, len(data[0])


def in_bounds(z):
    return i_min <= z.real < i_max and j_min <= z.imag < j_max


def neighbours(v, maze):
    zv, dv = v
    result = [((zv, CW[dv]), (1000, 0)), ((zv, CCW[dv]), (1000, 1))]
    if in_bounds(zv + dv.value) and maze.get(zv + dv.value) == '.':
        result.append(((zv + dv.value, dv), (1, 1)))
    return result



from time import perf_counter

t0 = perf_counter()
z0 = start, direction

visited = {z0}
frontier = set()
d = defaultdict(lambda: (math.inf, math.inf))
d[z0] = (0, 1)
for z, (c, l) in neighbours(z0, maze):
    frontier.add(z)
    d[z] = (c, l)

while frontier:
    if all(math.isinf(d[x][0]) for x in frontier):
        raise ValueError(frontier)
    current_node = min(frontier, key=lambda x: d[x][0])
    frontier.remove(current_node)
    visited.add(current_node)
    for z, (c, l) in neighbours(current_node, maze):
        if z in visited: continue
        frontier.add(z)
        current_c, current_len = d[current_node]
        if current_len < 0: print(current_node)
        d[z] = min(d[z], (current_c + c, current_len+l))

print(min((c, l-1) for (z, dz), (c, l) in d.items() if z == end))
print(perf_counter() - t0)

