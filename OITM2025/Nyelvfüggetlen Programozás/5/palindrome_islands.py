#!/usr/bin/env python3
from collections import Counter

def can_form_palindrome(digits):
    counts = Counter(digits)
    odd_count = sum(1 for count in counts.values() if count % 2 == 1)
    return odd_count <= 1

def count_palindrome_islands(filename):
    with open(filename, 'r') as f:
        grid = [line.rstrip('\n') for line in f]
    
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    
    visited = [[False] * cols for _ in range(rows)]
    
    def is_land(r, c):
        if 0 <= r < rows and 0 <= c < cols:
            return grid[r][c] != '~'
        return False
    
    def dfs(r, c, digits):
        visited[r][c] = True
        digits.append(grid[r][c])
        
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if is_land(nr, nc) and not visited[nr][nc]:
                    dfs(nr, nc, digits)
    
    palindrome_count = 0
    total_islands = 0
    
    for r in range(rows):
        for c in range(cols):
            if is_land(r, c) and not visited[r][c]:
                total_islands += 1
                digits = []
                dfs(r, c, digits)
                
                if can_form_palindrome(digits):
                    palindrome_count += 1
                    if palindrome_count <= 5:
                        print(f"Island {total_islands}: {''.join(digits)} -> Palindrome: Yes")
                elif total_islands <= 5:
                    print(f"Island {total_islands}: {''.join(digits)} -> Palindrome: No")
    
    return palindrome_count, total_islands

filename = "archipelago.txt"
palindrome_islands, total = count_palindrome_islands(filename)
print(f"Total islands: {total}")
print(f"Palindrome islands: {palindrome_islands}")
