from collections import defaultdict
from pathlib import Path


folder = Path(__file__).parent

with open(folder / 'input.txt') as handle:
    links = [line.strip().split('-') for line in handle.readlines() if line.strip()]
    inv_vertex_map, neighbours = {}, defaultdict(set)
    for v0, v1 in links:
        if v0 not in inv_vertex_map:
            inv_vertex_map[v0] = len(inv_vertex_map)
        i0 = inv_vertex_map[v0]
        if v1 not in inv_vertex_map:
            inv_vertex_map[v1] = len(inv_vertex_map)
        i1 = inv_vertex_map[v1]
        neighbours[i0].add(i1)
        neighbours[i1].add(i0)
    vertex_map = {v: k for k, v in inv_vertex_map.items()}

def translate(clique):
    return type(clique)(vertex_map[v] for v in clique)

print(vertex_map, )
# translated = {vertex_map[k]: {vertex_map[v] for v in vs} for k, vs in neighbours.items()}
# for k, v in translated.items():
#     print(k, v)
t_cliques = set()
t_vertices = [v for v, name in vertex_map.items() if name.startswith('t')]
for vt in t_vertices:
    for v1 in neighbours.get(vt, set()):
        for v2 in neighbours.get(v1, set()):
            if vt not in neighbours.get(v2, set()): continue
            clique = sorted({vt, v1, v2})
            if len(clique) < 3: continue
            t_cliques.add(tuple(clique))
# for c in t_cliques:
#     print(translate(c))
print(len(t_cliques))

cliques = []
for v0 in vertex_map.keys():
    clique = {v0}
    for v in vertex_map.keys():
        if v == v0: continue
        n = neighbours.get(v, set())
        if all(vc in n for vc in clique):
            clique.add(v)
    cliques.append(clique)

# for clique in cliques:
#     print(translate(sorted(clique)))
print(','.join(sorted(vertex_map[c] for c in max(cliques, key=len))))






