import heapq

def dijkstra(graph, start):
    heap = [(0, start)]
    visited = set()
    distances = {node: float('inf') for node in graph}
    distances[start] = 0

    while heap:
        (cost, current) = heapq.heappop(heap)

        if current in visited:
            continue

        visited.add(current)

        for neighbor, neighbor_cost in graph[current].items():
            if neighbor not in visited:
                new_cost = distances[current] + neighbor_cost
                if new_cost < distances[neighbor]:
                    distances[neighbor] = new_cost
                    heapq.heappush(heap, (new_cost, neighbor))

    return distances

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

    distances = dijkstra(graph, start_node)

    if distances[end_node] == float('inf'):
        print(f"There is no path from {start_node} to {end_node}.")
        return None
    else:
        return distances[end_node]

def main():
    filename = 'test_linkstate.txt'  # Replace with the actual filename
    graph = build_topology(filename)

    start_node = 'A'
    end_node = 'I'

    shortest_path = calculate_shortest_path(graph, start_node, end_node)

    if shortest_path is not None:
        print(f"Shortest path from {start_node} to {end_node}: {shortest_path}")

if __name__ == "__main__":
    main()
