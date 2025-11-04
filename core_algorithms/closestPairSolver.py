import math
import json

def euclidean_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def findClosestPair(points):
    if len(points) < 2:
        return {'distance': float('inf'), 'pair': None, 'total_points': len(points)}

    min_dist = float('inf')
    closest_pair = None

    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            p1 = points[i]['coords']
            p2 = points[j]['coords']
            dist = euclidean_distance(p1, p2)
            
            if dist < min_dist:
                min_dist = dist
                closest_pair = (points[i], points[j])
                
    if closest_pair:
        p1_info = closest_pair[0]
        p2_info = closest_pair[1]

        return {
            'distance': round(min_dist, 2),
            'pair_1_name': p1_info['name'],
            'pair_1_coords': p1_info['coords'],
            'pair_2_name': p2_info['name'],
            'pair_2_coords': p2_info['coords'],
            'total_points': len(points)
        }
    else:
        return {'distance': 0, 'pair': None, 'total_points': len(points)}

def loadProximityData():
    try:
        with open('data/coordinates.json') as f:
            data = json.load(f)
    except FileNotFoundError:
        return [], []

    # 1. Feature 8: Emergency Response (Uses all 50 points)
    emergency_points = []
    for i, p in enumerate(data):
        # Data structure is a list of dictionaries, accessing by keys 'name', 'x', 'y'
        emergency_points.append({
            'name': f"{p['name']}", 
            'coords': (p['x'], p['y']) 
        })
    
    # 2. Feature 9: Underserved Zones (Uses a subset of 4 points)
    underserved_indices = [8, 11, 25, 49] 
    
    underserved_points = []
    for i in underserved_indices:
        if i < len(data):
            p = data[i]
            underserved_points.append({
                'name': f"{p['name']} (Underserved)", 
                'coords': (p['x'], p['y'])
            })

    return emergency_points, underserved_points