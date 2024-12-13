from dataclasses import dataclass
from pathlib import Path
import re

folder = Path(__file__).parent


@dataclass
class Machine:
    x_A: int
    y_A: int
    x_B: int
    y_B: int
    x_prize: int
    y_prize: int

    def solutions(self):
        den_A = self.x_A * self.y_B - self.y_A * self.x_B
        if den_A == 0:
            raise ValueError(self)

        num_A = self.x_prize * self.y_B - self.y_prize * self.x_B
        if num_A / den_A != num_A // den_A:
            # No solutions
            return []

        n_A = num_A // den_A

        num_B = self.y_prize - self.y_A * n_A
        den_B = self.y_B
        if num_B / den_B != num_B // den_B:
            # Nope
            print(self)
            return []
        n_B = num_B // den_B
        return [(n_A, n_B)]


def cost(n_A, n_B) -> int:
    return 3 * n_A + n_B


def parse(part: str) -> Machine:
    m_A = re.search(r'Button A: X\+(\d+), Y\+(\d+)', part)
    m_B = re.search(r'Button B: X\+(\d+), Y\+(\d+)', part)
    m_prize = re.search(r'Prize: X=(\d+), Y=(\d+)', part)
    return Machine(
        x_A=int(m_A[1]),
        y_A=int(m_A[2]),
        x_B=int(m_B[1]),
        y_B=int(m_B[2]),
        x_prize=int(m_prize[1]),
        y_prize=int(m_prize[2]),
    )


with open(folder / 'input.txt') as handle:
    data = [parse(part) for part in handle.read().split('\n\n')]

print(sum(cost(*sol) for part in data for sol in part.solutions()))

new_data = [Machine(
    x_A=m.x_A,
    y_A=m.y_A,
    x_B=m.x_B,
    y_B=m.y_B,
    x_prize=m.x_prize + 10000000000000,
    y_prize=m.y_prize + 10000000000000,

) for m in data]
print(sum(cost(*sol) for part in new_data for sol in part.solutions()))
