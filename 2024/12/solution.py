from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional

folder = Path(__file__).parent

with open(folder / 'input.txt') as handle:
    data = [line.strip() for line in handle.readlines() if line.strip()]


@dataclass(slots=True)
class Plot:
    char: str
    points: set[tuple[int, int]]

    def __hash__(self):
        return hash((self.char, tuple(self.points)))

    def __eq__(self, other):
        return self.char == other.char and self.points == other.points

    def is_adjacent_point(self, i, j):
        return ((i - 1, j) in self.points
                or (i + 1, j) in self.points
                or (i, j - 1) in self.points
                or (i, j + 1) in self.points)

    def is_adjacent_plot(self, other: 'Plot') -> bool:
        return self.char == other.char and any(self.is_adjacent_point(i, j) for i, j in other.points)

    def add(self, i, j):
        self.points.add((i, j))

    @property
    def area(self) -> int:
        return len(self.points)

    @property
    def perimeter(self) -> int:
        result = 0
        for i, j in self.points:
            result += (i - 1, j) not in self.points
            result += (i + 1, j) not in self.points
            result += (i, j - 1) not in self.points
            result += (i, j + 1) not in self.points
        return result

    def _sides(self):
        result = []
        for i, j in self.points:
            if (i - 1, j) not in self.points:  # top
                result.append(Side(start=(i, j), end=(i, j + 1), t=SideType.up))
            if (i, j - 1) not in self.points:  # left
                result.append(Side(start=(i, j), end=(i + 1, j), t=SideType.left))
            if (i, j + 1) not in self.points:  # right
                result.append(Side(start=(i, j + 1), end=(i + 1, j + 1), t=SideType.right))
            if (i + 1, j) not in self.points:  # bottom
                result.append(Side(start=(i + 1, j), end=(i + 1, j + 1), t=SideType.down))
        return result

    @property
    def bulk_perimeter(self) -> int:
        side_set = self._sides()
        while True:
            new_side_set = []
            seen = set()
            for s0 in side_set:
                if s0 in seen:
                    continue
                seen.add(s0)
                for s1 in side_set:
                    if s1 in seen or s0 == s1:
                        continue
                    result = s0.merge(s1)
                    if result is not None:
                        seen.add(s1)
                        new_side_set.append(result)
                        break
                else:
                    new_side_set.append(s0)
            if len(new_side_set) == len(side_set):
                break
            else:
                side_set = new_side_set
        return len(side_set)


class SideType(Enum):
    left=0
    right=1
    up=2
    down=3

@dataclass
class Side:
    start: tuple[int, int]
    end: tuple[int, int]
    t: SideType

    def __hash__(self):
        return hash((self.start, self.end, self.t.value))

    def merge(self, other: 'Side') -> Optional['Side']:
        if self.t == other.t and self.start[0] == self.end[0] == other.start[0] == other.end[0]:
            if self.end[1] == other.start[1]:
                return Side(start=self.start, end=other.end, t=self.t)
            if self.start[1] == other.end[1]:
                return Side(start=other.start, end=self.end, t=self.t)
        if self.t == other.t and self.start[1] == self.end[1] == other.start[1] == other.end[1]:
            if self.end[0] == other.start[0]:
                return Side(start=self.start, end=other.end, t=self.t)
            if self.start[0] == other.end[0]:
                return Side(start=other.start, end=self.end, t=self.t)
        return None


# assert Side(start=(0, 0), end=(0, 1)).merge(Side(start=(0, 1), end=(1, 1))) is None
# assert Side(start=(0, 0), end=(0, 1)).merge(Side(start=(0, 1), end=(0, 2))) == Side(start=(0, 0), end=(0, 2))
# assert Side(start=(0, 1), end=(0, 2)).merge(Side(start=(0, 0), end=(0, 1))) == Side(start=(0, 0), end=(0, 2))


def merge(left: Plot, right: Plot) -> Plot:
    assert left.char == right.char
    return Plot(left.char, left.points | right.points)


def defrag(plots: list[Plot]):
    while True:
        print("=" * 100)
        print(len(plots))
        print("=" * 100)

        new_plots = []
        seen = set()
        for i, p0 in enumerate(plots):
            if i % 100 == 0: print(f'{i=}')
            if p0 in seen:
                continue
            seen.add(p0)

            for j, p1 in enumerate(plots):
                # print(f'{j=}')
                if p1 in seen or p0 == p1:
                    continue

                if p0.is_adjacent_plot(p1):
                    seen.add(p1)
                    new_plots.append(merge(p0, p1))
                    break
            else:
                new_plots.append(p0)
        if len(new_plots) == len(plots):
            break
        else:
            plots = new_plots
    return plots


points = [Plot(char=c, points={(i, j)}) for i, line in enumerate(data) for j, c in enumerate(line)]
plots = defrag(points)
print(sum(plot.area * plot.perimeter for plot in plots))
print(sum(plot.area * plot.bulk_perimeter for plot in plots))
