from copy import deepcopy
from enum import Enum
from functools import cmp_to_key
from itertools import pairwise
from pathlib import Path
from dataclasses import dataclass
from typing import Optional


class Operator(Enum):
    AND = lambda x, y: x and y
    OR = lambda x, y: x or y
    XOR = lambda x, y: x ^ y


@dataclass(slots=True, unsafe_hash=True)
class Instruction:
    i: int
    op: Operator
    x: str
    y: str
    out: str

    @classmethod
    def from_line(cls, line, i):
        inputs, out = line.split(' -> ')
        if ' AND ' in inputs:
            x, y = inputs.split(' AND ')
            return cls(i=i, op=Operator.AND, x=x.strip(), y=y.strip(), out=out.strip())
        if ' OR ' in inputs:
            x, y = inputs.split(' OR ')
            return cls(i=i, op=Operator.OR, x=x.strip(), y=y.strip(), out=out.strip())
        if ' XOR ' in inputs:
            x, y = inputs.split(' XOR ')
            return cls(i=i, op=Operator.XOR, x=x.strip(), y=y.strip(), out=out.strip())
        else:
            raise ValueError(f'Unrecognized input {line}')


folder = Path(__file__).parent

with open(folder / 'input.txt') as handle:
    raw_inputs, raw_instructions = handle.read().split("\n\n")
    inputs = {}
    for line in raw_inputs.split('\n'):
        if not line.strip(): continue
        var, val = line.split(':')
        inputs[var.strip()] = bool(int(val.strip()))
    lines = [line for line in raw_instructions.split('\n') if line.strip()]
    instructions = [Instruction.from_line(line, i) for i, line in enumerate(lines)]


def to_int(bits: dict[str, bool], f=lambda k: True) -> int:
    relevant = [x for k, x in reversed(sorted(bits.items())) if f(k)]
    return int(''.join('1' if x else '0' for x in relevant), base=2)


def to_bits(n: int, prefix: str = 'x', bit_len=4) -> dict[str, bool]:
    return {f'{prefix}{i:02}': b == '1' for i, b in enumerate(reversed(format(n, f'0{bit_len}b')))}


def execute(instructions, inputs):
    result = {}
    while instructions:
        skipped = []
        for i in instructions:
            if (i.x not in inputs and i.x not in result) or (i.y not in inputs and i.y not in result):
                skipped.append(i)
                continue
            x = inputs.get(i.x, result.get(i.x))
            y = inputs.get(i.y, result.get(i.y))
            result[i.out] = i.op(x, y)
        if len(skipped) == len(instructions):
            raise ValueError(f'No instructions executed {instructions=}')
        instructions = skipped
    return result


print(to_int(execute(deepcopy(instructions), deepcopy(inputs)), lambda k: k.startswith('z')))


def x(i: int) -> str:
    return f'x{i:02}'


def y(i: int) -> str:
    return f'y{i:02}'


# find inputs that depend on xi
def find_depending_on(var: str, instructions: list[Instruction]) -> set[Instruction]:
    direct = {i for i in instructions if i.x == var or i.y == var}
    return direct | {dep for i in direct for dep in find_depending_on(i.out, instructions)}


def find_ancestors(var: str, instructions: list[Instruction]) -> set[Instruction]:
    direct = {i for i in instructions if i.out == var}
    return (direct
            | {anc for i in direct for anc in find_ancestors(i.x, instructions)}
            | {anc for i in direct for anc in find_ancestors(i.y, instructions)})


def find_broken_first_broken(inputs, instructions) -> Optional[int]:
    instructions = deepcopy(instructions)

    original_inputs = inputs
    inputs = deepcopy(inputs)

    i_max = max(int(s.replace('x', '').replace('y', '')) for s in inputs.keys()) + 1
    for i in range(1, i_max):
        inputs[x(i)] = 0
        inputs[y(i)] = 0

    for i in range(1, i_max):
        x_ = to_int(inputs, lambda x: x.startswith('x'))
        y_ = to_int(inputs, lambda y: y.startswith('y'))
        expected = to_bits(x_ + y_, 'z', i_max + 1)
        result = execute(deepcopy(instructions), inputs)
        result_keys = sorted([k for k in result.keys() if k.startswith('z')])
        for k0, k1 in pairwise(result_keys):
            if result[k1] != expected[k1]:
                candidates = find_ancestors(k0, instructions) - find_ancestors(k1, instructions)
                print(candidates)
                return k0, k1
        inputs[x(i)] = original_inputs[x(i)]
        inputs[y(i)] = original_inputs[y(i)]


swapped = []
cnt = 0
while True:
    i = find_broken_first_broken(inputs, instructions)
    print(cnt, i)
    if i is None: break

    d_x0 = find_depending_on(x(i), instructions)
    d_y0 = find_depending_on(y(i), instructions)
    d_x1 = find_depending_on(x(i - 1), instructions)
    d_y1 = find_depending_on(y(i - 1), instructions)
    borked = list((d_x0 & d_y0) - d_x1 - d_y1)
    swapped.append(borked)
    assert len(borked) == 2

    out0, out1 = deepcopy(borked[0].out), deepcopy(borked[1].out)
    instructions[borked[0].i].out = out1
    instructions[borked[1].i].out = out0
    cnt += 1

print(borked)
