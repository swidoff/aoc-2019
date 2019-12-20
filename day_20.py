from collections import deque
from typing import Tuple

from networkx import Graph, shortest_path, compose


def donut_to_graph_portals(donut: str) -> Graph:
    nodes = {}
    mat = donut.split('\n')

    for r in range(1, len(mat) - 1):
        for c in range(1, len(mat[r]) - 1):
            char = mat[r][c]
            if char.isalpha():
                if mat[r + 1][c] == '.':
                    nodes[(r + 1, c)] = mat[r - 1][c] + char
                elif mat[r - 1][c] == '.':
                    nodes[(r - 1, c)] = char + mat[r + 1][c]
                elif mat[r][c + 1] == '.':
                    nodes[(r, c + 1)] = mat[r][c - 1] + char
                elif mat[r][c - 1] == '.':
                    nodes[(r, c - 1)] = char + mat[r][c + 1]

    graph = Graph()
    graph.add_nodes_from(nodes.values())

    queue = deque()
    for loc, node in nodes.items():
        queue.append((node, loc, 0))
    seen = set()
    while len(queue) > 0:
        node, loc, steps = queue.popleft()
        seen.add((node, loc))

        r, c = loc
        for new_loc in [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]:
            sym = mat[new_loc[0]][new_loc[1]]
            if (node, new_loc) in seen or sym != '.':
                continue

            if new_loc in nodes:
                if not graph.has_edge(node, nodes[new_loc]) or graph[node][nodes[new_loc]]['distance'] > steps + 1:
                    graph.add_edge(node, nodes[new_loc], distance=steps + 1)
            else:
                queue.append((node, new_loc, steps + 1))

    return graph


def shortest_path_steps(graph: Graph):
    path = shortest_path(graph, source='AA', target='ZZ', weight='distance')
    steps = 0
    for i in range(1, len(path)):
        steps += graph[path[i - 1]][path[i]]['distance']
    return steps + max(len(path) - 2, 0)


def problem1():
    with open('day_20_input.txt') as f:
        img = f.read()
    graph = donut_to_graph_portals(img)
    return shortest_path_steps(graph)


def donut_to_graphs_recursive(donut: str) -> Tuple[Graph, Graph]:
    nodes = {}
    mat = donut.split('\n')

    def suffix(r: int, c: int):
        return "_inner" if 2 <= r < len(mat) - 2 and 2 <= c < len(mat[0]) - 2 else "_outer"

    for r in range(1, len(mat) - 1):
        for c in range(1, len(mat[r]) - 1):
            char = mat[r][c]
            if char.isalpha():
                if mat[r + 1][c] == '.':
                    nodes[(r + 1, c)] = mat[r - 1][c] + char + suffix(r, c)
                elif mat[r - 1][c] == '.':
                    nodes[(r - 1, c)] = char + mat[r + 1][c] + suffix(r, c)
                elif mat[r][c + 1] == '.':
                    nodes[(r, c + 1)] = mat[r][c - 1] + char + suffix(r, c)
                elif mat[r][c - 1] == '.':
                    nodes[(r, c - 1)] = char + mat[r][c + 1] + suffix(r, c)

    outer_graph = Graph()
    inner_graph = Graph()
    for loc, node in nodes.items():
        if node in ('AA_outer', 'ZZ_outer') or node.endswith("_inner"):
            outer_graph.add_node(node)
        if node not in ('AA_outer', 'ZZ_outer'):
            inner_graph.add_node(node)

    queue = deque()
    for loc, node in nodes.items():
        queue.append((node, loc, 0))
    seen = set()
    while len(queue) > 0:
        node, loc, steps = queue.popleft()
        seen.add((node, loc))

        r, c = loc
        for new_loc in [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]:
            sym = mat[new_loc[0]][new_loc[1]]
            if (node, new_loc) in seen or sym != '.':
                continue

            if new_loc in nodes:
                target_node = nodes[new_loc]
                for graph in [inner_graph, outer_graph]:
                    if graph.has_node(node) and graph.has_node(target_node) and (
                            not graph.has_edge(node, target_node) or
                            graph[node][target_node]['distance'] > steps + 1
                    ):
                        graph.add_edge(node, target_node, distance=steps + 1)
            else:
                queue.append((node, new_loc, steps + 1))

    return outer_graph, inner_graph


def compose_graphs(outer_graph: Graph, inner_graph: Graph, levels: int = 100) -> Graph:
    def copy_graph(src: Graph, level: str) -> Graph:

        copy = Graph()
        for node in src.nodes:
            copy.add_node(node + level)
        for to_node, from_node, edge_data in src.edges.data():
            copy.add_edge(to_node + level, from_node + level, **edge_data)
        return copy

    res = copy_graph(outer_graph, '0')
    for level in range(1, levels):
        inner_copy = copy_graph(inner_graph, str(level))
        res = compose(res, inner_copy)
        for node in set(n[:2] for n in inner_graph.nodes):
            res.add_edge(node + "_inner" + str(level - 1), node + "_outer" + str(level), distance=1)

    return res


def shortest_path_steps_recursive(graph: Graph):
    path = shortest_path(graph, source='AA_outer0', target='ZZ_outer0', weight='distance')
    steps = 0
    for i in range(1, len(path)):
        steps += graph[path[i - 1]][path[i]]['distance']
    return steps


def problem2():
    with open('day_20_input.txt') as f:
        img = f.read()
    outer_graph, inner_graph = donut_to_graphs_recursive(img)
    graph = compose_graphs(outer_graph, inner_graph, 100)
    return shortest_path_steps_recursive(graph)


if __name__ == '__main__':
    # print(problem1())
    print(problem2())
