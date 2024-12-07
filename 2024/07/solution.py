import operator
from math import log10
from pathlib import Path
from typing import Callable

folder = Path(__file__).parent

data = []
with open(folder / 'input.txt') as handle:
    for line in handle.readlines():
        target, operands = line.split(':')
        data.append((int(target), [int(operand) for operand in operands.split()]))


def is_solvable(target: int, operands: list[int], operators: list[Callable[[int, int], int]]) -> bool:
    if len(operands) == 0:
        return False
    elif len(operands) == 1:
        return operands[0] == target
    else:
        first, second, *rest = operands
        return any(is_solvable(target, [op(first, second), *rest], operators) for op in operators)


print(sum(target for target, operands in data if is_solvable(target, operands, [operator.mul, operator.add])))


def combine(left: int, right: int) -> int:
    return left * 10 ** int(1 + log10(right)) + right


print(sum(target for target, operands in data if is_solvable(target, operands, [operator.mul, operator.add, combine])))
