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
