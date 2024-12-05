with open('input') as handle:
    data = [[int(x) for x in line.strip()] for line in handle.readlines()]


x_len = len(data)
y_len = len(data[0])

big_map = []
for x in range(5*x_len):
    i, x_inner = divmod(x, x_len)
    this_line = []
    for y in range(5*y_len):
        j, y_inner = divmod(y, y_len)
        new_value = data[x_inner][y_inner] + i + j
        if new_value >= 10:
            new_value = (new_value % 10) + 1
        this_line.append(new_value)
    big_map.append(this_line)

# print('\n'.join(''.join(str(x) for x in line) for line in big_map))

data = big_map

x_max = len(data) - 1
y_max = len(data[0]) - 1

data[0][0] = 0


def neighbours(x, y):
    if x > 0: yield (x-1, y)
    if y > 0: yield (x, y-1)
    if x < x_max: yield (x+1, y)
    if y < y_max: yield (x, y+1)


def points(n):
    for delta_x in range(n+1):
        delta_y = n-delta_x
        if x_max - delta_x < 0: continue
        if y_max - delta_y < 0: continue
        yield (x_max-delta_x, y_max-delta_y)



all_nodes = [(x, y) for x in range(len(data)) for y in range(len(data[0]))]

d = {(x, y): data[x][y] for x, y in all_nodes}
start = (0, 0)
goal = (x_max, y_max)

h = lambda n: n[0] + n[1] -1
open_set = {start}
came_from = {}
g_score = {p: float('inf') for p in all_nodes}
g_score[start] = 0
f_score = {p: float('inf') for p in all_nodes}
f_score[start] = 1
while open_set:
    # print(len(open_set))
    current = min(open_set, key=lambda n: f_score[n])
    if current == goal: break
    open_set.remove(current)
    for neighbour in neighbours(*current):
        tentative_g_score = g_score[current] + d[neighbour]
        if tentative_g_score < g_score[neighbour]:
            came_from[neighbour] = current
            g_score[neighbour] = tentative_g_score
            f_score[neighbour] = tentative_g_score + h(neighbour)
            open_set.add(neighbour)

print(g_score[x_max, y_max])
