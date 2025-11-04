import numpy as np

def solveKnapsack(projects, maxBudget):
    n = len(projects)
    
    weights = [p['cost'] for p in projects]
    values = [p['benefit'] for p in projects]
    names = [p['name'] for p in projects]

    K = np.zeros((n + 1, maxBudget + 1))

    for i in range(1, n + 1):
        for w in range(1, maxBudget + 1):
            if weights[i-1] <= w:
                K[i, w] = max(values[i-1] + K[i-1, w - weights[i-1]], K[i-1, w])
            else:
                K[i, w] = K[i-1, w]

    selectedProjects = []
    w = maxBudget
    for i in range(n, 0, -1):
        if K[i, w] != K[i-1, w]:
            selectedProjects.append(names[i-1])
            w -= weights[i-1]
            
    totalCost = sum(weights[i] for i, name in enumerate(names) if name in selectedProjects)

    return {
        'maxBenefit': K[n, maxBudget],
        'totalCost': totalCost,
        'selectedProjects': selectedProjects
    }