from collections import defaultdict
from typing import Dict, List, Tuple
from copy import deepcopy


class Graph:
    def __init__(self):
        self.adjacency_list: Dict[int, Dict[int, float]] = defaultdict(dict)
        self.user_features: Dict[int, List[int]] = {}
        self.original_adjacency_list: Dict[int, Dict[int, float]] = {}
        self.m = None

    def add_unweighted_edge(self, u: int, v: int):
        self.adjacency_list[u][v] = 1
        self.adjacency_list[v][u] = 1

    def remove_edge(self, u: int, v: int):
        del self.adjacency_list[u][v]
        del self.adjacency_list[v][u]

    def modify_weight(self, u: int, v: int, weight: float):
        self.adjacency_list[u][v] = weight
        self.adjacency_list[v][u] = weight

    def add_user_features(self, user_id: int, features: List[int]):
        self.user_features[user_id] = features

    def finish_initialization(self):
        self.original_adjacency_list = deepcopy(self.adjacency_list)
        self.m = sum(sum(self.original_adjacency_list[u].values()) for u in self.original_adjacency_list) / 2

    def vertex_pair_generator(self):
        for u in self.adjacency_list.keys():
            for v in self.adjacency_list.keys():
                if u != v:
                    yield u, v

    def get_unweighted_graph(self):
        unweighted_graph = defaultdict(dict)
        for u in self.adjacency_list.keys():
            for v in self.adjacency_list[u].keys():
                unweighted_graph[u][v] = 0

        return unweighted_graph

    def remaining_edges(self):
        return int(sum([len(self.adjacency_list[u]) for u in self.adjacency_list]) / 2)


def stdin_to_graph() -> Graph:
    graph = Graph()

    while True:
        line = input()
        if not line.strip():
            break

        line = line.strip()
        u, v = map(int, line.split())
        graph.add_unweighted_edge(u, v)

    while True:
        try:
            line = input()
        except EOFError:
            break

        line = line.strip()
        user_id, *features = map(int, line.split())
        graph.add_user_features(user_id, features)

    for u in graph.adjacency_list:
        for v in graph.adjacency_list[u]:
            max_similarity = len(graph.user_features[u])
            similarity = sum(a == b for a, b in zip(graph.user_features[u], graph.user_features[v]))
            diff = max_similarity - (similarity - 1)

            graph.modify_weight(u, v, diff)

    graph.finish_initialization()

    return graph


def modularity(graph: Graph) -> float:
    mod = 0
    for u in graph.original_adjacency_list:
        for v in graph.original_adjacency_list:

            delta = 1 if len(find_paths_between(graph, u, v)) > 0 else 0

            if u == v:
                delta = 1

            A = graph.original_adjacency_list[u].get(v, 0)
            k_u = sum(graph.original_adjacency_list[u].values())
            k_v = sum(graph.original_adjacency_list[v].values())

            mod += (A - (k_u * k_v / (2 * graph.m))) * delta

    return round((mod / (2 * graph.m)), 4)


def edge_betweenness(graph: Graph):
    btwns = graph.get_unweighted_graph()

    for u, v in graph.vertex_pair_generator():
        all_paths = find_paths_between(graph, u, v)
        if not all_paths:
            continue
        min_length = min([x[0] for x in all_paths])
        # print(f"{u=} {v=} {min_length=}")

        shortest_paths = [x for x in all_paths if x[0] == min_length]
        N = len(shortest_paths)

        for path in shortest_paths:
            path_vertices = path[1]
            for i in range(len(path_vertices) - 1):
                first = path_vertices[i]
                second = path_vertices[i + 1]

                btwns[first][second] += 1 / N

    return btwns


def find_paths_between(graph: Graph, u: int, v: int):
    paths: list[Tuple[float, List[int]]] = []

    def search(graph: Graph, current_node: int, end_node: int, path: Tuple[float, List[int]], depth=0):
        neighbours = graph.adjacency_list[current_node].keys()

        for neighbour in neighbours:
            if neighbour in path[1]:
                continue

            extended_path: [Tuple[float, List[int]]] = (
                path[0] + graph.adjacency_list[current_node][neighbour], path[1] + [neighbour])
            if neighbour == end_node:
                paths.append(extended_path)
                continue

            search(graph, neighbour, end_node, extended_path, depth + 1)

    search(graph, u, v, (0, [u]), 0)

    return paths


def find_biggest_betweennesses(b_graph: Dict[int, Dict[int, float]]):
    biggest_betweenness = float('-inf')

    edges_to_remove = []

    for u in b_graph.keys():
        for v in b_graph[u].keys():
            betweenness = b_graph[u][v]
            if betweenness > biggest_betweenness:
                edges_to_remove = [sorted([u, v])]
                biggest_betweenness = betweenness
            elif betweenness == biggest_betweenness and sorted([u, v]) not in edges_to_remove:
                edges_to_remove.append(sorted([u, v]))

    return edges_to_remove


def detect_communities(graph: Graph):
    class Community:
        def __init__(self):
            self.vertices = set()
            self.list = []

        def add_vertex(self, vertex):
            self.vertices.add(vertex)
            self.list = sorted(list(self.vertices))

        def contains(self, vertex):
            return vertex in self.vertices

        def __str__(self):
            return "-".join(map(str, self.list))

        def __len__(self):
            return len(self.list)

    communities: List[Community] = []

    for u, v in graph.vertex_pair_generator():
        if len(find_paths_between(graph, u, v)) > 0:
            found = False
            for community in communities:
                if community.contains(u) or community.contains(v):
                    community.add_vertex(u)
                    community.add_vertex(v)
                    found = True
                    break

            if not found:
                new_community = Community()
                new_community.add_vertex(u)
                new_community.add_vertex(v)
                communities.append(new_community)

    for u in graph.user_features.keys():
        if u not in graph.adjacency_list.keys():
            new_community = Community()
            new_community.add_vertex(u)
            communities.append(new_community)

    communities.sort(key=lambda x: (len(x), x.list[0]), reverse=False)

    return communities


if __name__ == "__main__":
    G = stdin_to_graph()

    best_mod = modularity(G)
    best_partition = detect_communities(G)
    while G.remaining_edges() != 0:
        btwns = edge_betweenness(G)
        biggest = find_biggest_betweennesses(btwns)

        biggest = sorted(biggest)

        for pair in biggest:
            print(pair[0], pair[1])
            G.remove_edge(*pair)

        communities = detect_communities(G)

        if modularity(G) > best_mod:
            best_mod = modularity(G)
            best_partition = communities

    output = ""

    for community in best_partition:
        output += str(community) + " "

    output = output.strip()

    print(output)
