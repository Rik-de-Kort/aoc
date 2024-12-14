from copy import deepcopy
from pathlib import Path
import re

folder = Path(__file__).parent

with open(folder / 'input.txt') as handle:
    matches = [re.match(r'p=(\d+),(\d+) v=(-?\d+),(-?\d+)', line) for line in handle.readlines()]
    data = [((int(m[1]), int(m[2])), (int(m[3]), int(m[4]))) for m in matches]

# positive x -> moving to right
# positive y -> moving down
min_x, x_max = 0, 101
min_y, y_max = 0, 103


def step(robots):
    new_robots = []
    for (x, y), (dx, dy) in robots:
        new_robots.append((((x + dx) % x_max, (y + dy) % y_max), (dx, dy)))
    return new_robots


x_mid = x_max // 2
y_mid = y_max // 2


def safety_factor(robots):
    q0, q1, q2, q3 = 0, 0, 0, 0
    for (x, y), _ in robots:
        q0 += x < x_mid and y < y_mid
        q1 += x < x_mid and y > y_mid
        q2 += x > x_mid and y < y_mid
        q3 += x > x_mid and y > y_mid
    return q0 * q1 * q2 * q3


robots = deepcopy(data)
for i in range(100):
    robots = step(robots)

print(safety_factor(robots))


def display(robots):
    lines = [[0 for _ in range(x_max)] for _ in range(y_max)]
    for (x, y), _ in robots:
        lines[y][x] += 1
    print('\n'.join(
        ''.join('.' if x == 0 else str(x) for x in line)
        for line in lines
    ))


robots = deepcopy(data)
i = 0
while True:
    print(i)
    i += 1
    robots = step(robots)
    if all((x == x_ and y == y_) for ((x, y), _), ((x_, y_), __) in zip(robots, data)):
        break
    if i % 101 == 68:
        display(robots)
        input()
