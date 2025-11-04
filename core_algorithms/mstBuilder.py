import networkx as nx

def buildMST(G):
    mstEdges = list(nx.minimum_spanning_edges(G, data=True))
    
    totalCost = sum(d['weight'] for u, v, d in mstEdges)
    
    edgeList = [f"({u} - {v}) Cost: {d['weight']}" for u, v, d in mstEdges]
    
    return {
        'cost': totalCost,
        'edges': edgeList
    }