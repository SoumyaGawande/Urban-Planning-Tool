import numpy as np
import math

def getOrientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - \
          (q[0] - p[0]) * (r[1] - q[1])
    
    if val == 0: 
        return 0
        
    return 1 if val > 0 else 2 

def getSquaredDistance(p1, p2):
    return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2

def runGrahamScan(pointsArray):
    
    if len(pointsArray) < 3:
        return list(pointsArray)

    allPoints = [tuple(p) for p in pointsArray]

    startPoint = min(allPoints, key=lambda p: (p[1], p[0]))
    
    pointsList = allPoints[:]
    pointsList.remove(startPoint)
    
    def getPolarAngleSortKey(point):
        angle = math.atan2(point[1] - startPoint[1], point[0] - startPoint[0])
        distance = getSquaredDistance(startPoint, point)
        return (angle, distance)

    pointsListWithAngle = []
    for point in pointsList:
        angle = math.atan2(point[1] - startPoint[1], point[0] - startPoint[0])
        distance = getSquaredDistance(startPoint, point)
        pointsListWithAngle.append((angle, distance, point))
        
    pointsListWithAngle.sort()
    
    pointsList = [p[2] for p in pointsListWithAngle]

    m = 1
    for i in range(1, len(pointsList)):
        while i < len(pointsList) and \
              getOrientation(startPoint, pointsList[m-1], pointsList[i]) == 0:
            i += 1
        
        if i < len(pointsList):
            pointsList[m] = pointsList[i]
            m += 1
            
    pointsList = pointsList[:m]

    if len(pointsList) < 2:
        return [startPoint]

    hullStack = [startPoint, pointsList[0]] 
    
    for i in range(1, len(pointsList)):
        pNext = pointsList[i]
        
        while len(hullStack) > 1 and getOrientation(hullStack[-2], hullStack[-1], pNext) != 2:
            hullStack.pop()
            
        hullStack.append(pNext)
        
    return hullStack

def calculatePolygonArea(hullPoints):
    xCoords = [p[0] for p in hullPoints]
    yCoords = [p[1] for p in hullPoints]
    
    area = 0.0
    numPoints = len(hullPoints)
    for i in range(numPoints):
        j = (i + 1) % numPoints
        area += (xCoords[i] * yCoords[j])
        area -= (xCoords[j] * yCoords[i])
        
    return abs(area) / 2.0

def buildConvexHull(pointsList):
    
    coords = [(point['x'], point['y']) for point in pointsList]
    
    if len(coords) < 3:
        return {'hullPointsStr': "Requires at least 3 points.", 'area': 0, 'error': "Requires at least 3 points."}
        
    try:
        hullCoords = runGrahamScan(np.array(coords))
        
        area = calculatePolygonArea(hullCoords)
        
        originalPointsMap = {tuple([point['x'], point['y']]): point['name'] for point in pointsList}
        
        hullPointsStringList = []
        for xCoord, yCoord in hullCoords:
            name = originalPointsMap.get((xCoord, yCoord), "Unknown Point")
            hullPointsStringList.append(f"{name} ({xCoord}, {yCoord})")

        return {
            'hullPointsStr': "\n".join(hullPointsStringList),
            'area': round(area, 2),
            'error': None
        }
        
    except Exception as e:
        return {'hullPointsStr': "Calculation failed.", 'area': 0, 'error': f"Hull calculation failed: {e}"}