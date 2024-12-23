from functools import cache
from pathlib import Path

folder = Path(__file__).parent

with open(folder / 'input.txt') as handle:
    raw_towels, raw_targets = handle.read().split("\n\n")
    towels = [towel.strip() for towel in raw_towels.split(', ')]
    targets = [target.strip() for target in raw_targets.splitlines()]

print(towels)
print(targets)

@cache
def is_solvable(target, towels):
    if target == '':
        return True
    candidates = []
    for towel in towels:
        if target.startswith(towel):
            candidates.append(target[len(towel):])
    return any(is_solvable(candidate, towels) for candidate in candidates)

# assert is_solvable('brwrr', towels)
# assert not is_solvable('bbrgwb', towels)

print(sum(is_solvable(target, tuple(towels)) for target in targets))

@cache
def n_solutions(target, towels):
    if target == '':
        return 1
    candidates = set()
    for towel in towels:
        if target.startswith(towel):
            candidates.add(target[len(towel):])
    return sum(n_solutions(candidate, towels) for candidate in candidates)

print(sum(n_solutions(target, tuple(towels)) for target in targets))
