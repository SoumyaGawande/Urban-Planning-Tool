import heapq
import networkx as nx
from collections import defaultdict

def solveDijkstra(G, startNode, endNode):
    """
    Manually implements Dijkstra's Algorithm to find the shortest path 
    in a graph G (NetworkX object) with non-negative 'weight' edges.
    """
    
    # 1. Input Validation and Graph Conversion
    if startNode not in G or endNode not in G:
        return {'path': f"Error: Invalid Node ({startNode} or {endNode})", 'distance': 0}

    # Extract nodes and edges into simple Python structures
    # Node keys: node ID strings
    # Edges: u -> v mapped to weight (cost)
    
    # Using NetworkX iterators to extract weights is clean
    # Graph is assumed to be bidirectional based on how it's built in app.py
    distances = {node: float('inf') for node in G.nodes}
    predecessors = {node: None for node in G.nodes}
    
    distances[startNode] = 0
    
    # Priority Queue: stores tuples of (distance, node)
    priorityQueue = [(0, startNode)] 

    # 2. Main Dijkstra's Loop
    while priorityQueue:
        currentDistance, currentNode = heapq.heappop(priorityQueue)

        # If we found a longer path to currentNode previously, skip it
        if currentDistance > distances[currentNode]:
            continue

        # If we reached the target, we can stop
        if currentNode == endNode:
            break

        # Explore neighbors (using standard NetworkX neighbors view)
        for neighbor in G.neighbors(currentNode):
            weight = G[currentNode][neighbor].get('weight', 1)
            distance = currentDistance + weight

            # Relaxation step: If a shorter path is found
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = currentNode
                heapq.heappush(priorityQueue, (distance, neighbor))

    # 3. Path Reconstruction
    
    if distances[endNode] == float('inf'):
        return {'path': "No path found.", 'distance': 0}

    path = []
    current = endNode
    while current is not None:
        path.append(current)
        current = predecessors[current]
    
    # Path is built backward, so reverse it
    path.reverse()

    return {
        'path': " -> ".join(path), 
        'distance': distances[endNode]
    }