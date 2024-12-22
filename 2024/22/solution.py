import math
from collections import Counter, defaultdict
from functools import cache
from itertools import pairwise
from pathlib import Path

from tqdm import tqdm

folder = Path(__file__).parent

with open(folder / 'input.txt') as handle:
    seeds = [int(line.strip()) for line in handle.readlines() if line.strip()]

print(seeds)


def mix(a, b):
    return a ^ b


assert mix(42, 15) == 37


def prune(n):
    return n % 16777216


assert prune(100000000) == 16113920


@cache
def get_next(n: int) -> int:
    n = prune(mix(n, n * 64))
    n = prune(mix(n, n // 32))
    n = prune(mix(n, n * 2048))
    return n


assert get_next(123) == 15887950


def run_n_times(n, f, start):
    result = start
    for _ in range(n):
        result = f(result)
    return result


N = 2000

# print(sum(run_n_times(N, get_next, seed) for seed in seeds))

secrets = seeds
prices = [[(secret % 10) for secret in secrets]]
for _ in range(1, N):  # skip first iteration
    secrets = [get_next(secret) for secret in secrets]
    prices.append([secret % 10 for secret in secrets])

prices = list(zip(*prices))
assert len(prices) == len(seeds) and all(len(p) == N for p in prices)

deltas = [[p1 - p0 for p0, p1 in pairwise(p)] for p in prices]
assert len(deltas) == len(seeds) and all(len(d) == N-1 for d in deltas)
assert all(d[j] == p[j+1] - p[j] for d, p in zip(deltas, prices) for j in range(len(d)))

assert list(range(10))[6:10] == [6, 7, 8, 9]  # range(len(d) - 4 + 1) (len(d) = 10, include 6)

Seq = tuple
Seller = int
Price = int
buyers: dict[Seq, dict[Seller, Price]] = defaultdict(dict)
for i_buyer, (p, d) in enumerate(zip(prices, deltas)):
    for j in range(len(d) - 4 + 1):
        seq = tuple(d[j:j+4])
        price = p[j]
        if i_buyer not in buyers[seq]:
            buyers[seq][i_buyer] = price

max_seq = max(buyers.keys(), key=lambda seq: sum(buyers[seq].values()))
print(max_seq, sum(buyers[max_seq].values()))
