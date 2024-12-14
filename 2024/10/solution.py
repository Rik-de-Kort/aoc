from pathlib import Path

folder = Path(__file__).parent

with open(folder / 'input.txt') as handle:
    data = [[int(c) if c != '.' else -10 for c in line.strip()] for line in handle.readlines()]


def display(trail_map):
    print('\n'.join(
        ''.join(str(i) if i >= 0 else '.' for i in line)
        for line in trail_map
    ))


i_min, i_max = 0, len(data)
j_min, j_max = 0, len(data[0])


def in_bounds(i, j):
    return i_min <= i < i_max and j_min <= j < j_max


def score(start, trail_map, seen=None):
    seen = set() if seen is None else seen
    if start in seen:
        return 0
    seen.add(start)

    i, j = start
    if data[i][j] == 9:
        return 1

    next_steps = []
    i_next, j_next = i - 1, j  # up
    if in_bounds(i_next, j_next) and data[i_next][j_next] == data[i][j] + 1:
        next_steps.append((i_next, j_next))
    i_next, j_next = i, j - 1  # left
    if in_bounds(i_next, j_next) and data[i_next][j_next] == data[i][j] + 1:
        next_steps.append((i_next, j_next))
    i_next, j_next = i + 1, j  # down
    if in_bounds(i_next, j_next) and data[i_next][j_next] == data[i][j] + 1:
        next_steps.append((i_next, j_next))
    i_next, j_next = i, j + 1  # right
    if in_bounds(i_next, j_next) and data[i_next][j_next] == data[i][j] + 1:
        next_steps.append((i_next, j_next))
    return sum(score(step, trail_map, seen) for step in next_steps)


trailheads = [(i, j) for i in range(i_min, i_max) for j in range(j_min, j_max) if data[i][j] == 0]
print(sum(score(th, data) for th in trailheads))


def rating(start, trail_map, seen=None):
    # seen = set() if seen is None else seen
    # if start in seen:
    #     return 0
    # seen.add(start)

    i, j = start
    if data[i][j] == 9:
        return 1

    next_steps = []
    i_next, j_next = i - 1, j  # up
    if in_bounds(i_next, j_next) and data[i_next][j_next] == data[i][j] + 1:
        next_steps.append((i_next, j_next))
    i_next, j_next = i, j - 1  # left
    if in_bounds(i_next, j_next) and data[i_next][j_next] == data[i][j] + 1:
        next_steps.append((i_next, j_next))
    i_next, j_next = i + 1, j  # down
    if in_bounds(i_next, j_next) and data[i_next][j_next] == data[i][j] + 1:
        next_steps.append((i_next, j_next))
    i_next, j_next = i, j + 1  # right
    if in_bounds(i_next, j_next) and data[i_next][j_next] == data[i][j] + 1:
        next_steps.append((i_next, j_next))
    return sum(rating(step, trail_map, seen) for step in next_steps)


print(sum(rating(th, data) for th in trailheads))
