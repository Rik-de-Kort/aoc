class P:
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __lt__(self, other):
        return (self.x, self.y, self.z) < (other.x, other.y, other.z)

    def __ge__(self, other):
        return (self.x, self.y, self.z) >= (other.x, other.y, other.z)

    def __iter__(self):
        return iter((self.x, self.y, self.z))

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __repr__(self):
        return f'P({self.x}, {self.y}, {self.z})'
    
    def __sub__(self, other):
        return P(self.x - other.x, self.y - other.y, self.z - other.z)

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z

    def __add__(self, other):
        return P(self.x + other.x, self.y + other.y, self.z + other.z)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z

# Figure out this rotation business
class T:
    def __init__(self, direction):
        self.direction = direction
        self.minus = False

    def __eq__(self, other):
        return self.direction == other.direction and self.minus == other.minus

    def __hash__(self):
        return hash((self.direction, self.minus))

    def __neg__(self):
        self.minus = not self.minus
        return self

    def __repr__(self):
        if self.minus:
            return self.direction
        else:
            return '-'+self.direction

rotate_along_x = lambda p: P(p.x, -p.z, p.y)
rotate_along_y = lambda p: P(-p.z, p.y, p.x)
rotate_along_z = lambda p: P(p.y, -p.x, p.z)
nothing = lambda p: p

from itertools import combinations_with_replacement
from functools import partial

rotation_points = set()
for f0, f1, f2, f3, f4 in combinations_with_replacement([rotate_along_x, rotate_along_y, rotate_along_z, nothing], 5):
    rotation_points.add(f0(f1(f2(f3(f4(P(T('x'), T('y'), T('z'))))))))

def rotate_by(pt, p):
    return P(
        -getattr(p, pt.x.direction) if pt.x.minus else getattr(p, pt.x.direction),
        -getattr(p, pt.y.direction) if pt.y.minus else getattr(p, pt.y.direction),
        -getattr(p, pt.z.direction) if pt.z.minus else getattr(p, pt.z.direction),
    )

from collections import OrderedDict

def fingerprint(beacons):
    fp = OrderedDict()
    for b0 in sorted(beacons):
        for b1 in sorted(beacons):
            if b1 >= b0 or (b0, b1) in fp: continue
            fp[b0, b1] = b1 - b0
    assert len(fp) == len(beacons) * (len(beacons)-1) / 2
    assert all((b0, b1) in fp.keys() or (b1, b0) in fp.keys() for b0, b1 in product(beacons, beacons) if b0 != b1)
    return fp


from itertools import product

def from_pov_of(first, second):
    fp0 = fingerprint(first)
    for phi in rotation_points:
        rotated = sorted([rotate_by(phi, p) for p in second])
        fp1 = fingerprint(rotated)

        # matching_edges = {}
        # deltas = set()
        # n_overlap = 0
        # for (source, sink), diff in fp0.items():
        #     for (source_, sink_), diff_ in fp1.items():
        #         if diff != diff_: continue
        #         deltas.add(source - source_)
        #         deltas.add(sink - sink_)
        #         # deltas.add(source_ - source)
        #         # deltas.add(sink_ - sink)
        #         n_overlap += 1
        # print(n_overlap)
        # if n_overlap < 66: continue

        overlap = set(fp0.values()) & set(fp1.values())
        if len(overlap) < 66: continue  # 12*11 / 2

        # Figure out which points map to which
        matching_edges = {}
        for edge, diff in fp0.items():
            if diff not in overlap: continue
            matching_edges[edge] = [e for e, d in fp1.items() if d == diff][0]
        # print(len(matching_edges))
        # for e1, e2 in matching_edges.items():
        #     print(e1)
        #     print(e2)
        #     print('-'*10)

        deltas = set()
        # matching_points = {}
        for (p10, p11), (p00, p01) in matching_edges.items():
            # matching_points[p10] = p00
            # matching_points[p11] = p01
            deltas.add(p10 - p00)
            deltas.add(p11 - p01)

        # for p0, p1 in matching_points.items(): print(p0, p1)
        assert len(deltas) == 1
        delta = next(iter(deltas))
        # return matching_points
        return {rotate_by(phi, p) + delta for p in second}, delta
        

def path(g, start, end, visited=None):
    visited = set() if visited is None else visited
    if start == end: return []
    elif (start, end) in g: return [(start, end)]
    for source in [source for (source, sink) in g if sink == end and source not in visited]:
        result = path(g, start, source, visited | {end})
        if result is not None: return result + [(source, end)]

with open('input') as handle:
    blocks = handle.read().split('\n\n')
    data = [sorted(P(*eval(line)) for line in block.split('\n')[1:] if line) for block in blocks]


result = set(data[0])
frontier = {0}
final = set()
scanner_positions = []
while frontier:
    print(frontier, len(data) - len(final))
    i = frontier.pop()
    final.add(i)
    for j in [j for j in range(len(data)) if j not in final]:
        attempt = from_pov_of(result, data[j])
        if attempt is not None:
            attempt, position = attempt
            result |= attempt
            scanner_positions.append(position)
            frontier.add(j)

print(len(result))

# print(scanner_positions)

def manhattan(p, q):
    return sum(abs(c) for c in p - q)

print(max(manhattan(p, q) for p in scanner_positions for q in scanner_positions))
