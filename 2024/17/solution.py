from copy import deepcopy
from dataclasses import dataclass
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
    p: int
    A: int
    B: int
    C: int
    output: list[int]


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
        state.A = state.A // (2**get_combo_value(combo, state))
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
        state.B = state.A // (2**get_combo_value(combo, state))
        state.p += 2
    elif instr == 7:  # cdv
        state.C = state.A // (2**get_combo_value(combo, state))
        state.p += 2
    return state


state = State(
    p=0,
    A=a,
    B=b,
    C=c,
    output=[]
)
# print(state)
while state.p+1 < len(instrs):
    # print(state.p)
    instr, combo = instrs[state.p], instrs[state.p+1]
    # print(instr, combo)
    state = exec_instr(instr, combo, state)

print(','.join(str(x) for x in state.output))