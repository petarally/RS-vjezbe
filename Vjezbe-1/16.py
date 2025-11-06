def dijkstra(graph, start):
    import heapq
    nodes = set(graph) | {v for nbrs in graph.values() for v, _ in nbrs}
    nodes.add(start)
    distances = {n: float('inf') for n in nodes}
    distances[start] = 0

    pq = [(0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if d != distances[u]:
            continue

        for v, w in graph.get(u, []):
            nd = d + w
            if nd < distances[v]:
                distances[v] = nd
                heapq.heappush(pq, (nd, v))

    return {k: distances[k] for k in sorted(distances)}


graph = {
    'A': [('B', 1), ('C', 4)],
    'B': [('A', 1), ('C', 2), ('D', 5)],
    'C': [('A', 4), ('B', 2), ('D', 1)],
    'D': [('B', 5), ('C', 1)]
}

print(dijkstra(graph, 'A'))  