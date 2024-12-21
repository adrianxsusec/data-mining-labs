from collections import defaultdict

WHITE_NODE = 0
BLACK_NODE = 1


class Graph:
    def __init__(self):
        self.vertices = dict()
        self.edges = defaultdict(list)

    def add_vertex(self, index, type_):
        self.vertices[index] = type_

    def add_edge(self, first, second):
        self.edges[first].append(second)
        self.edges[second].append(first)

    def all_black_nodes_distance(self, max_distance=10):
        n = len(self.vertices)
        distances = [-1] * n
        nearest_black_node = [-1] * n
        queue = list()

        for node, type_ in self.vertices.items():
            if type_ == 1:
                queue.append(node)
                distances[node] = 0
                nearest_black_node[node] = node

        while queue:
            current = queue.pop(0)
            current_distance = distances[current]
            if current_distance >= max_distance:
                continue
            for neighbor in self.edges[current]:
                if distances[neighbor] == -1:
                    distances[neighbor] = current_distance + 1
                    nearest_black_node[neighbor] = nearest_black_node[current]
                    queue.append(neighbor)
                elif distances[neighbor] == current_distance + 1:
                    if nearest_black_node[neighbor] > nearest_black_node[current]:
                        nearest_black_node[neighbor] = nearest_black_node[current]

        result = list(zip(nearest_black_node, distances))
        return result


def load_data():
    graph = Graph()
    n, e = map(int, input().strip().split())

    for index in range(n):
        type_ = int(input().strip())
        graph.add_vertex(index, type_)

    for _ in range(e):
        first, second = map(int, input().strip().split())
        graph.add_edge(first, second)

    return graph


if __name__ == "__main__":
    graph = load_data()
    results = graph.all_black_nodes_distance()
    for black_node, distance in results:
        print(black_node, distance)
