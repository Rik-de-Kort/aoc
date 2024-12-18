from copy import deepcopy
from dataclasses import dataclass, field
from pathlib import Path

folder = Path(__file__).parent

with open(folder / 'input.txt') as handle:
    registers, program = handle.read().split('\n\n')
    registers = registers.split('\n')
    a = int(registers[0].split(':')[1].strip())
    b = int(registers[1].split(':')[1].strip())
    c = int(registers[2].split(':')[1].strip())

    instrs = [int(x) for x in program.split(':')[1].strip().split(',')]


@dataclass(slots=True)
class State:
    A: int
    B: int
    C: int
    p: int = 0
    output: list[int] = field(default_factory=list)


def get_combo_value(combo: int, state: State):
    return {
        0: 0,
        1: 1,
        2: 2,
        3: 3,
        4: state.A,
        5: state.B,
        6: state.C
    }[combo]


def exec_instr(instr: int, combo: int, state: State) -> State:
    if instr == 0:  # Adv
        state.A = state.A // (2 ** get_combo_value(combo, state))
        state.p += 2
    elif instr == 1:  # bxl
        state.B = state.B ^ combo
        state.p += 2
    elif instr == 2:  # bst
        state.B = get_combo_value(combo, state) % 8
        state.p += 2
    elif instr == 3:  # jnz
        if state.A != 0:
            state.p = combo
        else:
            state.p += 2
    elif instr == 4:  # bxc
        state.B = state.B ^ state.C
        state.p += 2
    elif instr == 5:  # combo
        state.output.append(get_combo_value(combo, state) % 8)
        state.p += 2
    elif instr == 6:  # bdv
        state.B = state.A // (2 ** get_combo_value(combo, state))
        state.p += 2
    elif instr == 7:  # cdv
        state.C = state.A // (2 ** get_combo_value(combo, state))
        state.p += 2
    return state


def run_program(instrs, state):
    while state.p + 1 < len(instrs):
        instr, combo = instrs[state.p], instrs[state.p + 1]
        state = exec_instr(instr, combo, state)
    return state


print(','.join(str(x) for x in run_program(instrs, State(A=a, B=b, C=c)).output))


def is_postfix(left, right):
    return len(left) <= len(right) and all(x == y for x, y in zip(left, right[-len(left):]))


for a in range(1, 100):
    before = run_program(instrs, State(A=a, B=0, C=0)).output
    for k in range(8):
        after = run_program(instrs, State(A=8 * a + k, B=0, C=0)).output
        assert is_postfix(before, after), (a, k, before, after)

candidates = [0]
for i, target in enumerate(reversed(instrs)):
    new_candidates = []
    for c in candidates:
        for k in range(8):
            candidate = 8 * c + k
            out = run_program(instrs, State(A=candidate, B=0, C=0)).output
            if out[-(i + 1)] == target:
                new_candidates.append(candidate)
    assert new_candidates
    candidates = new_candidates
print(min(candidates))
