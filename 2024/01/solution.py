from collections import Counter
from pathlib import Path

folder = Path(__file__).parent

with open(folder / 'input.txt') as handle:
    data = [[int(x) for x in line.split()] for line in handle.readlines()]

left, right = zip(*data)
print(sum(abs(x - y) for x, y in zip(sorted(left), sorted(right))))

c = Counter(right)
print(sum(x * c.get(x, 0) for x in left))