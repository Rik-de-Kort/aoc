from pathlib import Path

folder = Path(__file__).parent

with open(folder / 'input.txt') as handle:
    data = [[int(x) for x in line.split()] for line in handle.readlines()]


def is_safe(line):
    is_monotone = all(x < y for x, y in zip(line[:-1], line[1:])) or all(x > y for x, y in zip(line[:-1], line[1:]))
    is_bound = all(abs(x - y) <= 3 for x, y in zip(line[:-1], line[1:]))
    return is_monotone and is_bound


print(sum(is_safe(line) for line in data))
print(sum(any(is_safe(line[:i] + line[i + 1:]) for i in range(len(line))) for line in data))
