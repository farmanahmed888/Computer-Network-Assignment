import heapq

def dijkstra(graph, start):
    heap = [(0, start, None)]
    visited = set()
    distances = {node: float('inf') for node in graph}
    predecessors = {node: None for node in graph}
    distances[start] = 0

    while heap:
        (cost, current, predecessor) = heapq.heappop(heap)

        if current in visited:
            continue

        visited.add(current)
        predecessors[current] = predecessor

        for neighbor, neighbor_cost in graph[current].items():
            if neighbor not in visited:
                new_cost = distances[current] + neighbor_cost
                if new_cost < distances[neighbor]:
                    distances[neighbor] = new_cost
                    heapq.heappush(heap, (new_cost, neighbor, current))

    return predecessors

def build_topology(filename):
    graph = {}
    
    with open(filename, 'r') as file:
        for line in file:
            start, end, cost = line.split()
            cost = int(cost)

            if start not in graph:
                graph[start] = {}

            if end not in graph:
                graph[end] = {}

            graph[start][end] = cost
            graph[end][start] = cost

    return graph

def calculate_shortest_path(graph, start_node, end_node):
    if start_node not in graph or end_node not in graph:
        print(f"Start or end node not found in the topology.")
        return None

    predecessors = dijkstra(graph, start_node)

    if predecessors[end_node] is None:
        print(f"There is no path from {start_node} to {end_node}.")
        return None
    else:
        path = []
        current = end_node

        while current is not None:
            path.insert(0, current)
            current = predecessors[current]

        return path

def main():
    filename = 'test_linkstate.txt'  
    graph = build_topology(filename)

    start_node = 'A'
    end_node = 'I'

    path = calculate_shortest_path(graph, start_node, end_node)

    if path is not None:
        print(f"Shortest path from {start_node} to {end_node}: {' -> '.join(path)}")

if __name__ == "__main__":
    main()
