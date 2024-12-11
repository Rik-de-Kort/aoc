from functools import cache

from math import log10, ceil
from pathlib import Path

folder = Path(__file__).parent

with open(folder / 'input.txt') as handle:
    data = [int(c.strip()) for c in handle.read().split()]


def step(stone: int) -> list[int]:
    if stone == 0:
        return [1]

    n_digits = int(log10(stone) + 1)
    if n_digits % 2 == 0:
        left, right = divmod(stone, 10**(n_digits // 2))
        return [left, right]

    return [stone * 2024]


assert step(0) == [1]
assert step(1) == [2024]
assert step(10) == [1, 0]
assert step(99) == [9, 9]
assert step(999) == [2021976]


stones = data
for j in range(25):
    stones = [new_stone for stone in stones for new_stone in step(stone)]
print(len(stones))


@cache
def get_length(stone: int, n_steps=5) -> int:
    if n_steps == 0:
        return 1
    else:
        return sum(get_length(stone, n_steps-1) for stone in step(stone))


print(sum(get_length(stone, n_steps=75) for stone in data))