from flask import Flask, render_template, request
import json
import networkx as nx

from core_algorithms.shortestPath import solveDijkstra
from core_algorithms.knapsackSolver import solveKnapsack
from core_algorithms.mstBuilder import buildMST
from core_algorithms.convexHullBuilder import buildConvexHull
from core_algorithms.nQueenPlacement import findSensorPlacement 
from core_algorithms.closestPairSolver import findClosestPair, loadProximityData 

app = Flask(__name__)

def loadNetworkData():
    with open('data/city_network.json') as f:
        data = json.load(f)
    
    G = nx.Graph()
    for node in data['nodes']:
        G.add_node(node['id'], name=node['name'])
    
    for u, v, weight in data['edges']:
        G.add_edge(u, v, weight=weight)
    return G

def loadProjectsData():
    with open('data/projects.json') as f:
        return json.load(f)

def loadCoordinatesData():
    with open('data/coordinates.json') as f:
        return json.load(f)

def loadNetworkEdgesForDisplay():
    with open('data/city_network.json') as f:
        data = json.load(f)
    
    formatted_edges = [f"{u} <--> {v} (Cost: {w})" for u, v, w in data['edges']]
    return formatted_edges


def getRenderContext(activeResultKey=None, activeResultValue=None):
    emergency_points, underserved_points = loadProximityData()
    
    networkData = loadNetworkData()
    networkNodes = [{'id': n[0], 'name': n[1]['name']} for n in networkData.nodes(data=True)]
    
    all_network_edges = loadNetworkEdgesForDisplay()
    
    context = {
        'networkNodes': networkNodes,
        'all_network_edges': all_network_edges,
        'emergency_points': emergency_points, 
        'underserved_points': underserved_points, 
        
        'dijkstraResult': None,
        'knapsackResult': None,
        'mstResult': None,
        'hullResult': None,
        'sensorResult': None,
        'proximityResult': None,
    }
    
    if activeResultKey:
        context[activeResultKey] = activeResultValue
        
    return context


@app.route('/')
def home():
    return render_template('index.html', **getRenderContext())


@app.route('/solve-dijkstra', methods=['POST'])
def handleDijkstra():
    startNode = request.form['startNode'].upper()
    endNode = request.form['endNode'].upper()
    G = loadNetworkData()
    result = solveDijkstra(G, startNode, endNode)
    return render_template('index.html', **getRenderContext('dijkstraResult', result))

@app.route('/solve-knapsack', methods=['POST'])
def handleKnapsack():
    try:
        maxBudget = int(request.form['maxBudget'])
    except ValueError:
        maxBudget = 0
    projects = loadProjectsData()
    result = solveKnapsack(projects, maxBudget)
    return render_template('index.html', **getRenderContext('knapsackResult', result))

@app.route('/solve-mst', methods=['POST'])
def handleMST():
    G = loadNetworkData()
    result = buildMST(G)
    return render_template('index.html', **getRenderContext('mstResult', result))

@app.route('/solve-hull', methods=['POST'])
def handleHull():
    points = loadCoordinatesData()
    result = buildConvexHull(points)
    return render_template('index.html', **getRenderContext('hullResult', result))

@app.route('/solve-sensors', methods=['POST'])
def handleSensorPlacement():
    try:
        n = int(request.form['numSensors'])
    except ValueError:
        n = 0
        
    if n > 14 or n < 1:
        result = {'n': n, 'success': False, 'coordinates': [], 'count': 0, 'visualGrid': "Input N must be between 1 and 14 for stable calculation."}
        return render_template('index.html', **getRenderContext('sensorResult', result))
        
    result = findSensorPlacement(n)
    return render_template('index.html', **getRenderContext('sensorResult', result))


@app.route('/check-proximity', methods=['POST'])
def handleProximityChecker():
    emergency_points, _ = loadProximityData()
    result = findClosestPair(emergency_points)
    return render_template('index.html', **getRenderContext('proximityResult', result))


if __name__ == '__main__':
    app.run(debug=True)