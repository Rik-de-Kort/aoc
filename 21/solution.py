with open('test_input') as handle:
    positions = [int(line.split(': ')[1].strip()) for line in handle.readlines()]

print(positions)

class Die:
    def __init__(self):
        self.count = 0

    def roll(self):
        self.count += 1
        return self.count


die = Die()
scores = [0, 0]
while True:
    # Player 0
    steps = sum(die.roll() for _ in range(3))
    positions[0] = (positions[0] + steps) % 10
    scores[0] += positions[0] if positions[0] > 0 else 10
    if scores[0] >= 1000: break

    steps = sum(die.roll() for _ in range(3))
    positions[1] = (positions[1] + steps) % 10
    scores[1] += positions[1]
    if scores[1] >= 1000: break

losing_score = scores[0] if scores[0] < 1000 else scores[1]
n_rolls = die.count
print(n_rolls)
print(losing_score * n_rolls)

from itertools import product
from copy import copy
from functools import cache

@cache
def calculate_wins(positions, scores, turn):
    if scores[0] >= 21: return 1, 0
    if scores[1] >= 21: return 0, 1

    wins_0, wins_1 = 0, 0
    for roll in product([1, 2, 3], [1, 2, 3], [1, 2, 3]):
        these_positions, these_scores = list(positions), list(scores)
        steps = sum(roll)
        these_positions[turn] = (these_positions[turn] + steps) % 10
        these_scores[turn] += these_positions[turn] if these_positions[turn] > 0 else 10
        from_here_0, from_here_1 = calculate_wins(tuple(these_positions), tuple(these_scores), 1 if turn == 0 else 0)
        wins_0 += from_here_0
        wins_1 += from_here_1
    return wins_0, wins_1


assert calculate_wins((4, 8), (21, 0), 1) == (1, 0)
assert calculate_wins((4, 8), (20, 0), 0) == (27, 0)
assert calculate_wins((4, 8), (0, 20), 0) == (0, 27*27)

with open('input') as handle:
    positions = [int(line.split(': ')[1].strip()) for line in handle.readlines()]

print(positions)
print(calculate_wins(tuple(positions), (0, 0), 0))
