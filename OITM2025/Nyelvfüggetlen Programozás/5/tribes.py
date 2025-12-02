from collections import deque

def read_map(filename):
    with open(filename, 'r') as f:
        return [line.rstrip('\n') for line in f]

def find_islands(grid):
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    visited = [[False] * cols for _ in range(rows)]
    islands = []
    
    def dfs(r, c, cells):
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return
        if visited[r][c] or grid[r][c] == '~':
            return
        
        visited[r][c] = True
        cells.add((r, c))
        dfs(r-1, c, cells)
        dfs(r+1, c, cells)
        dfs(r, c-1, cells)
        dfs(r, c+1, cells)
    
    for i in range(rows):
        for j in range(cols):
            if not visited[i][j] and grid[i][j] != '~':
                cells = set()
                dfs(i, j, cells)
                islands.append(cells)
    
    return islands

def bfs_water_distance(grid, start_cells, end_cells, max_distance):
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    queue = deque()
    visited = set()
    
    for r, c in start_cells:
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '~':
                if (nr, nc) not in visited:
                    queue.append((nr, nc, 1))
                    visited.add((nr, nc))
    while queue:
        r, c, dist = queue.popleft()
        
        if dist > max_distance:
            continue
        
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if (nr, nc) in end_cells:
                    return dist

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if grid[nr][nc] == '~' and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append((nr, nc, dist + 1))
    
    return float('inf')

def find_tribes(islands, grid, max_distance=10):
    n = len(islands)
    parent = list(range(n))
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        px, py = find(x), find(y)
        if px != py:
            parent[px] = py
    
    for i in range(n):
        for j in range(i + 1, n):
            dist = bfs_water_distance(grid, islands[i], islands[j], max_distance)
            if dist <= max_distance:
                union(i, j)
    
    tribes = len(set(find(i) for i in range(n)))
    return tribes

def main():
    grid = read_map('archipelago.txt')
    
    islands = find_islands(grid)
    print(f"Total islands: {len(islands)}")
    tribes = find_tribes(islands, grid, max_distance=10)
    print(f"Total tribes: {tribes}")

if __name__ == '__main__':
    main()
