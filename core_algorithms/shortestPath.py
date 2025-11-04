import heapq
import networkx as nx
from collections import defaultdict

def solveDijkstra(G, startNode, endNode):
   
    if startNode not in G or endNode not in G:
        return {'path': f"Error: Invalid Node ({startNode} or {endNode})", 'distance': 0}

   
    distances = {node: float('inf') for node in G.nodes}
    predecessors = {node: None for node in G.nodes}
    
    distances[startNode] = 0
    

    priorityQueue = [(0, startNode)] 

    while priorityQueue:
        currentDistance, currentNode = heapq.heappop(priorityQueue)

       
        if currentDistance > distances[currentNode]:
            continue

      
        if currentNode == endNode:
            break

       
        for neighbor in G.neighbors(currentNode):
            weight = G[currentNode][neighbor].get('weight', 1)
            distance = currentDistance + weight

   
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = currentNode
                heapq.heappush(priorityQueue, (distance, neighbor))

  
    
    if distances[endNode] == float('inf'):
        return {'path': "No path found.", 'distance': 0}

    path = []
    current = endNode
    while current is not None:
        path.append(current)
        current = predecessors[current]
    
    
    path.reverse()

    return {
        'path': " -> ".join(path), 
        'distance': distances[endNode]
    }