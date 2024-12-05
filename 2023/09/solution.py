with open('input') as handle:
    data = {(row, column): int(char) for row, line in enumerate(handle.readlines()) for column, char in enumerate(line.strip())}

def neighbourhood(x, y):
    return [(x, y-1), (x, y+1), (x-1, y), (x+1, y)]

low_points = [(x, y) for (x, y), value in data.items() if all(data.get(c, 10) > value for c in neighbourhood(x, y))]
print(sum(data[k] for k in low_points) + len(low_points))

from functools import reduce
import operator as op

def set_union(sets):
    return reduce(op.ior, sets)

basins = [{(x, y)} for x, y in low_points]
for _ in range(8):  # 10000 points in input, 4*7 > 10000, 8 iterations should do the trick
    for i, basin in enumerate(basins):
        basins[i] |= set_union({c for c in neighbourhood(*point) if c not in basin and data.get(c, 9) < 9} for point in basin)

sorted_lens = sorted(len(basin) for basin in basins)
print(sorted_lens[-1]*sorted_lens[-2]*sorted_lens[-3])
