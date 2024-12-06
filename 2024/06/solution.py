from copy import deepcopy
from pathlib import Path
from enum import Enum

import tqdm

folder = Path(__file__).parent


class MapTile(Enum):
    FREE = 0
    OBSTACLE = 1


def to_map_tile(c):
    return MapTile.FREE if c in ('.', '^') else MapTile.OBSTACLE


with open(folder / 'input.txt') as handle:
    data = [list(line.strip()) for line in handle.readlines()]
    i_start, j_start = [(i, j) for i, row in enumerate(data) for j, c in enumerate(row) if c == '^'][0]
    i_dir, j_dir = (-1, 0)  # up
    data = [[to_map_tile(c) for c in row] for row in data]

turn_right = {
    (-1, 0): (0, 1),
    (0, 1): (1, 0),
    (1, 0): (0, -1),
    (0, -1): (-1, 0),
}

i_min, i_max = 0, len(data)
j_min, j_max = 0, len(data[0])

i_guard, j_guard = i_start, j_start
visited = set()
while True:
    visited.add((i_guard, j_guard))
    if (i_guard + i_dir < i_min or i_max <= i_guard+i_dir
        or j_guard + j_dir < j_min or j_max <= j_guard + j_dir):
        break
    if data[i_guard + i_dir][j_guard + j_dir] == MapTile.FREE:
        i_guard += i_dir
        j_guard += j_dir
    else:
        i_dir, j_dir = turn_right[i_dir, j_dir]
print(len(visited))


loops = set()
to_check = [(i, j) for i in range(i_max) for j in range(j_max) if i != i_start or j != j_start]
for i, j in tqdm.tqdm(to_check):
    if data[i][j] == MapTile.OBSTACLE: continue
    data[i][j] = MapTile.OBSTACLE

    i_guard, j_guard = i_start, j_start
    i_dir, j_dir = (-1, 0)

    visited = set()
    while True:
        # print(((i_guard, j_guard), (i_dir, j_dir)))
        if ((i_guard, j_guard), (i_dir, j_dir)) in visited:
            # print(f'looping on {i, j}')
            # print(visited)
            loops.add((i, j))
            break
        visited.add(((i_guard, j_guard), (i_dir, j_dir)))
        if (i_guard + i_dir < i_min or i_max <= i_guard+i_dir
                or j_guard + j_dir < j_min or j_max <= j_guard + j_dir):
            break
        if data[i_guard + i_dir][j_guard + j_dir] == MapTile.FREE:
            i_guard += i_dir
            j_guard += j_dir
        else:
            i_dir, j_dir = turn_right[i_dir, j_dir]
    data[i][j] = MapTile.FREE
print(len(loops))
