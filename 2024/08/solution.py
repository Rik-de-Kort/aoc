from collections import defaultdict
from itertools import combinations
from pathlib import Path

folder = Path(__file__).parent

data = defaultdict(list)
with open(folder / 'input.txt') as handle:
    raw = [line.strip() for line in handle.readlines()]
    i_max, j_max = len(raw), len(raw[0])
    for i, line in enumerate(raw):
        for j, c in enumerate(line):
            if c.isalnum():
                data[c].append((i, j))


def display(antinodes):
    # Used to realize I wasn't stripping `\n` off the lines
    key_to_char = {k: c for c, v in data.items() for k in v}
    for (i, j) in antinodes:
        if (i, j) not in key_to_char:
            key_to_char[(i, j)] = '#'
    print('\n'.join(
        ''.join(key_to_char.get((i, j), '.') for j in range(j_max))
        for i in range(i_max)
    ))


i_min, j_min = 0, 0
antinodes = set()
for nodes in data.values():
    for (i0, j0), (i1, j1) in combinations(nodes, r=2):
        iv, jv = i1 - i0, j1 - j0

        ic, jc = i1 + iv, j1 + jv
        if (i_min <= ic < i_max) and (j_min <= jc < j_max):
            antinodes.add((ic, jc))

        ic, jc = i0 - iv, j0 - jv
        if (i_min <= ic < i_max) and (j_min <= jc< j_max):
            antinodes.add((ic, jc))

print(len(antinodes))

antinodes = set()
for nodes in data.values():
    for (i0, j0), (i1, j1) in combinations(nodes, r=2):
        iv, jv = i1 - i0, j1 - j0
        k = 0
        while (i_min <= (ic := i0 + k*iv) < i_max) and (j_min <= (jc := j0 + k*jv) < j_max):
            antinodes.add((ic, jc))
            k += 1
        k = -1
        while (i_min <= (ic := i0 + k*iv) < i_max) and (j_min <= (jc := j0 + k*jv) < j_max):
            antinodes.add((ic, jc))
            k -= 1

print(len(antinodes))
