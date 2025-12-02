def count_islands(filename):
    with open(filename, 'r') as f:
        grid = [line.rstrip('\n') for line in f]
    
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    
    visited = [[False] * cols for _ in range(rows)]
    
    def is_land(r, c):
        if 0 <= r < rows and 0 <= c < cols:
            return grid[r][c] != '~'
        return False
    
    def dfs(r, c):
        visited[r][c] = True

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if is_land(nr, nc) and not visited[nr][nc]:
                    dfs(nr, nc)
    island_count = 0
    for r in range(rows):
        for c in range(cols):
            if is_land(r, c) and not visited[r][c]:
                island_count += 1
                dfs(r, c)
    
    return island_count

filename = "archipelago.txt"
num_islands = count_islands(filename)
print(f"Number of islands: {num_islands}")
