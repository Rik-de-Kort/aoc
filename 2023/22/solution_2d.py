with open('input') as handle:
    lines = [line.strip().split() for line in handle.readlines()]
    ranges = []
    for (txt, rng) in lines:
        raw_x, raw_y, raw_z = rng.split(',')
        x_start, x_end = tuple(sorted(int(x) for x in raw_x.removeprefix('x=').split('..')))
        y_start, y_end = tuple(sorted(int(y) for y in raw_y.removeprefix('y=').split('..')))
        z_start, z_end = tuple(sorted(int(z) for z in raw_z.removeprefix('z=').split('..')))
        ranges.append((((x_start, y_start), (x_end, y_end)), txt=='on'))

print(ranges[:10])

from itertools import product 

def valid(rectangle):
    (x_start, y_start), (x_end, y_end) = rectangle
    return x_start < x_end and y_start < y_end

def inside(container, rectangle):
    (x0_start, y0_start), (x0_end, y0_end) = rectangle
    (x1_start, y1_start), (x1_end, y1_end) = container
    return x1_start <= x0_start <= x0_end <= x1_end and y1_start <= y0_start <= y0_end <= y1_end

def overlap_split(first, second):
    """Split 2 rectangles into overlapping areas"""
    (x0_start, y0_start), (x0_end, y0_end) = first
    (x1_start, y1_start), (x1_end, y1_end) = second
    xs = sorted([x0_start, x0_end, x1_start, x1_end])
    ys = sorted([y0_start, y0_end, y1_start, y1_end])
    x_ranges = xs[0:2], xs[1:3], xs[2:4]
    y_ranges = ys[0:2], ys[1:3], ys[2:4]

    candidates = [tuple(zip(xs_, ys_)) for xs_, ys_ in product(x_ranges, y_ranges)]
    candidates = [rect for rect in candidates if valid(rect)]
    overlap = [rect for rect in candidates if inside(first, rect) and inside(second, rect)]
    split = [rect for rect in candidates if inside(first, rect) or inside(second, rect) and rect not in overlap]
    return overlap, split

first = ranges[0][0]
second = ranges[1][0]

first = ((0, 0), (4, 4))
second = ((3, 3), (7, 7))
print('split')
for rect in overlap_split(first, second): print(rect)

print(list(zip((0, 0), (1, 2))))
