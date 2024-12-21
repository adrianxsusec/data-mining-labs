import timeit
from collections import defaultdict
from typing import List, Any, Tuple, Dict


class Graph:
    def __init__(self, beta):
        self.beta = beta
        self.vertices = set()
        self.neighbors = dict()

    def add_neighbors(self, origin: int, neighbors: List[int]):
        self.vertices.add(origin)
        self.vertices.update(neighbors)
        self.neighbors[origin] = neighbors

def load_graph() -> Tuple[Graph, Dict[int, List[Tuple[int, int]]], int]:
    number_vertices, beta = map(float, input().strip().split())
    graph = Graph(beta)

    for origin in range(int(number_vertices)):
        neighbors = list(map(int, input().strip().split()))
        graph.add_neighbors(origin, neighbors)

    q = int(input().strip())
    max_iteration = 0

    reqs = defaultdict(list)
    for req_index in range(q):
        vertex, iteration = map(int, input().strip().split())
        max_iteration = max(max_iteration, iteration)
        reqs[iteration].append((req_index, vertex))

    return graph, reqs, max_iteration

def node_rank(graph: Graph, reqs: Dict[int, List[Tuple[int, int]]], max_iteration: int):
    N = len(graph.vertices)
    rank = {vertex: 1 / N for vertex in graph.vertices}
    query_results = N * [None]

    for iteration in range(1, max_iteration + 1):
        new_rank = {vertex: 0 for vertex in graph.vertices}
        accumulator = 0

        for vertex in graph.vertices:
            if graph.neighbors.get(vertex, None) is None:
                continue

            vertex_rank = graph.beta * rank[vertex] / len(graph.neighbors[vertex])

            for neighbor in graph.neighbors[vertex]:
                new_rank[neighbor] += vertex_rank
                accumulator += vertex_rank

        for vertex in graph.vertices:
            new_rank[vertex] += (1 - accumulator) / N

        rank = new_rank.copy()

        for req_index, vertex in reqs[iteration]:
            query_results[req_index] = rank[vertex]

    return query_results


if __name__ == '__main__':
    graph, reqs, max_iteration = load_graph()
    start_time = timeit.default_timer()

    query_results = node_rank(graph, reqs, max_iteration)

    for result in query_results:
        print(f"{result:.10f}")
