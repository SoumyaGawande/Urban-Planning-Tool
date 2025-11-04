def generateGrid(n, placement):
    grid = []
    
    for _ in range(n):
        grid.append(['.'] * n)
        
    for row, col in placement:
        if 0 <= row < n and 0 <= col < n:
            grid[row][col] = 'S'
            
    gridString = "\n".join([" ".join(row) for row in grid])
    return gridString

def solveNQueens(n):
    board = [-1] * n
    solutions = []

    def isSafe(row, col):
        for prevRow in range(row):
            if board[prevRow] == col:
                return False
            if abs(row - prevRow) == abs(col - board[prevRow]):
                return False
        return True

    def solve(row):
        if row == n:
            solution = [(r, board[r]) for r in range(n)]
            solutions.append(solution)
            return

        for col in range(n):
            if isSafe(row, col):
                board[row] = col
                solve(row + 1)
                board[row] = -1

    solve(0)
    return solutions

def findSensorPlacement(n):
    solutions = solveNQueens(n)
    
    if solutions:
        firstPlacement = solutions[0]
        coords = [f"({r}, {c})" for r, c in firstPlacement]
        
        visualGrid = generateGrid(n, firstPlacement) 
        
        return {
            'n': n,
            'success': True,
            'coordinates': coords,
            'count': len(solutions),
            'visualGrid': visualGrid
        }
    else:
        return {
            'n': n,
            'success': False,
            'coordinates': [],
            'count': 0,
            'visualGrid': "N/A"
        }