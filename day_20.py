from collections import deque
from typing import List, Dict, Tuple

import networkx as nx
from networkx import Graph


def donut_to_graph(donut: str) -> Graph:
    """
    Creates a graph from the donut maze where each door is a node and the edges are the paths between the doors
    labeled with a distance. Nodes are named "XX_inner" for inner doors and "XX_outer" for outer doors. The graph
    has no connection between the inner and outer doors of the same code. That is done downstream.
    """
    mat = donut.split('\n')
    nodes = locate_nodes(mat)
    graph = create_graph(mat, nodes)
    return graph


def create_graph(mat: List[str], nodes: Dict[Tuple[int, int], str]) -> Graph:
    """
    Given the locations of the nodes on the maps, create a graph with edges between doors that have a path between
    them labled with the distance in steps.
    """
    graph = Graph()
    for loc, node in nodes.items():
        graph.add_node(node)

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
                if not graph.has_edge(node, target_node) or graph[node][target_node]['distance'] > steps + 1:
                    graph.add_edge(node, target_node, distance=steps + 1)
            else:
                queue.append((node, new_loc, steps + 1))
    return graph


def locate_nodes(mat: List[str]) -> Dict[Tuple[int, int], str]:
    """
    Returns a map containing the location of nodes mapped to their labels.
    """
    nodes = {}

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

    return nodes


def donut_to_graph_portals(donut: str) -> Graph:
    graph = donut_to_graph(donut)

    # Link the inner doors to the outer doors, distance = 1.
    for node in set(n[:2] for n in graph.nodes):
        graph.add_edge(node + "_inner", node + "_outer", distance=1)
    return graph


def shortest_path_steps(graph: Graph, source: str, target: str) -> int:
    path = nx.shortest_path(graph, source=source, target=target, weight='distance')
    steps = 0
    for i in range(1, len(path)):
        steps += graph[path[i - 1]][path[i]]['distance']
    return steps


def shortest_path_steps_portals(img: str) -> int:
    graph = donut_to_graph_portals(img)
    return shortest_path_steps(graph, "AA_outer", "ZZ_outer")


def problem1():
    with open('day_20_input.txt') as f:
        img = f.read()
    return shortest_path_steps_portals(img)


def donut_to_graphs_recursive(donut: str, levels: int) -> Graph:
    graph = donut_to_graph(donut)

    # Split the graph into the two prototypes -- the outer level and the inner levels.
    outer_graph = graph.copy()
    inner_graph = graph.copy()

    outer_graph.remove_nodes_from([
        n for n in graph.nodes
        if n.endswith("_outer") and n not in ("AA_outer", "ZZ_outer")
    ])
    inner_graph.remove_nodes_from(["AA_outer", "ZZ_outer"])

    def copy_graph(src: Graph, suffix: str) -> Graph:
        return nx.relabel_nodes(src, lambda n: n + suffix, copy=True)

    # Link the inner doors of each level - 1 with the outer doors of level.
    res = copy_graph(outer_graph, '0')
    for level in range(1, levels):
        inner_copy = copy_graph(inner_graph, str(level))
        res = nx.compose(res, inner_copy)
        for node in set(n[:2] for n in inner_graph.nodes):
            res.add_edge(node + "_inner" + str(level - 1), node + "_outer" + str(level), distance=1)

    return res


def shortest_path_steps_recursive(img: str):
    graph = donut_to_graphs_recursive(img, 100)
    return shortest_path_steps(graph, "AA_outer0", "ZZ_outer0")


def problem2():
    with open('day_20_input.txt') as f:
        img = f.read()
    return shortest_path_steps_recursive(img)


if __name__ == '__main__':
    print(problem1())  # 510
    print(problem2())  # 5652
