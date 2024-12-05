from collections import defaultdict

with open('input') as handle:
    data = [line.strip().split('-') for line in handle.readlines()]

graph = defaultdict(set)
for source, sink in data:
    graph[source].add(sink)
    graph[sink].add(source)

def find_routes(start_node, end_node, graph, small_visited, already_visited_twice):
    small_visited = small_visited.copy()
    if start_node == end_node: return [[]]
    if end_node.islower():
        if end_node in small_visited and already_visited_twice: return []
        elif end_node in small_visited:
            if end_node in ('start', 'end'): return []
            else: already_visited_twice = True
        else: small_visited.add(end_node)

    result = []
    for node in graph[end_node]:
        these_routes = find_routes(start_node, node, graph, small_visited, already_visited_twice)
        result.extend([route + [(node, end_node)] for route in these_routes])
    return result

print(len(find_routes('start', 'end', graph, set(), False)))
