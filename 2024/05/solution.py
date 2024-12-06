from functools import cmp_to_key
from pathlib import Path

folder = Path(__file__).parent

with open(folder / 'input.txt') as handle:
    ordering, pages_spec = handle.read().split('\n\n')
    ordering = [tuple(int(x) for x in line.split('|')) for line in ordering.split('\n')]
    pages_spec = [[int(x) for x in line.split(',')] for line in pages_spec.split('\n')]


def is_correct(pages: list[int]):
    for i, p0 in enumerate(pages[:-1]):
        for j, p1 in enumerate(pages[i + 1:]):
            for before, after in ordering:
                if p0 == after and p1 == before:
                    return False
    return True


def get_middle(items: list):
    if len(items) % 2 == 0: raise ValueError(f'only odd length pls')
    return items[len(items) // 2]


assert get_middle([75, 47, 61, 53, 29]) == 61

print(sum(get_middle(pages) for pages in pages_spec if is_correct(pages)))

to_be_fixed = [pages for pages in pages_spec if not is_correct(pages)]
def sort_fn(x: int, y: int):
    if (x, y) in ordering:
        return -1
    elif (y, x) in ordering:
        return 1
    else:
        return 0

print(sum(get_middle(sorted(pages, key=cmp_to_key(sort_fn))) for pages in pages_spec if not is_correct(pages)))
