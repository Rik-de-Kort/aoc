with open('input') as handle:
    data = [line.split('->') for line in handle.readlines()]
    data = [(start.strip().split(','), end.strip().split(',')) for start, end in data]
    data = [((int(x_0), int(y_0)), (int(x_1), int(y_1))) for ((x_0, y_0), (x_1, y_1)) in data]

def print_grid(g):
    x_max = max(x for x, y in g.keys())
    y_max = max(y for x, y in g.keys())
    result = []
    for y in range(y_max+1):
        line = []
        for x in range(x_max+1):
            here = g.get((x, y), 0)
            line.append(str(here) if here else '.')
        result.append(''.join(line))
    print('\n'.join(result))

from collections import defaultdict
grid = defaultdict(lambda: 0) 

# print(len(data), len(lines))

for (x_0, y_0), (x_1, y_1) in data:
    if x_0 == x_1 and y_0 < y_1:
        for i in range(y_1-y_0+1): grid[(x_0, y_0+i)] += 1
    elif x_0 == x_1 and y_0 > y_1:
        for i in range(y_0-y_1+1): grid[(x_0, y_1+i)] += 1
    elif x_0 < x_1 and y_0 == y_1:
        for i in range(x_1-x_0+1): grid[(x_0+i, y_0)] += 1
    elif x_0 > x_1 and y_0 == y_1:
        for i in range(x_0-x_1+1): grid[(x_1+i, y_0)] += 1
    elif x_0 < x_1 and y_0 < y_1:
        for i in range(x_1-x_0+1): grid[(x_0+i, y_0+i)] += 1
    elif x_0 < x_1 and y_0 > y_1:
        for i in range(x_1-x_0+1): grid[(x_0+i, y_0-i)] += 1
    elif x_0 > x_1 and y_0 < y_1:
        for i in range(x_0-x_1+1): grid[(x_1+i, y_1-i)] += 1
    elif x_0 > x_1 and y_0 > y_1:
        for i in range(x_0-x_1+1): grid[(x_1+i, y_1+i)] += 1
    else:
        raise ValueError(f'single point: {x_0, y_0, x_1, y_1}')
    # print((x_0, y_0), '->', (x_1, y_1))
    # print_grid(grid)
    # print('')

print(sum(v >= 2 for v in grid.values()))
