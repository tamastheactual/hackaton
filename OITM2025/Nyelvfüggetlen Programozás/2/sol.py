import numpy as np
from collections import deque

def parse_lego_file(filename):
    """Parse the ajandek.txt file containing LEGO brick data."""
    with open(filename, 'r') as f:
        content = f.read().strip()
    
    lines = content.split('\n')
    n = int(lines[0].strip())
    
    # Parse all hex values
    all_hex_values = []
    for line in lines[1:]:
        hex_values = line.strip().split()
        all_hex_values.extend(hex_values)
    
    return n, all_hex_values

def analyze_bricks(hex_values):
    """
    Analyze LEGO bricks and return statistics.
    
    Hex format: CLYXX
    - C (digit 0): Color [0=white, 1=red, 2=yellow]
    - L (digit 1): Level from bottom [0-8]
    - Y (digit 2): Y position front-to-back [0-14 in hex = 0-e]
    - X (digit 3): X position left-to-right [0-14 in hex = 0-e]
    """
    white_count = 0
    red_count = 0
    yellow_count = 0
    
    brick_positions = []
    
    for hex_val in hex_values:
        color_code = int(hex_val[0], 16)
        level = int(hex_val[1], 16)
        y_pos = int(hex_val[2], 16)
        x_pos = int(hex_val[3], 16)
        
        if color_code == 0:
            white_count += 1
        elif color_code == 1:
            red_count += 1
        elif color_code == 2:
            yellow_count += 1
        
        brick_positions.append((x_pos, y_pos, level))
    
    return {
        'white': white_count,
        'red': red_count,
        'yellow': yellow_count,
        'total': len(hex_values),
        'positions': brick_positions
    }

def build_3d_grid(brick_positions):
    """Build a 3D grid representing the LEGO structure."""
    # Create 3D grid: dimensions are 15x15x9 (X: 0-14, Y: 0-14, Z/Level: 0-8)
    # 0 = empty, 1 = has brick
    grid = np.zeros((15, 15, 9), dtype=int)
    
    for x, y, z in brick_positions:
        grid[x, y, z] = 1
    
    return grid

def find_interior_cavity(grid):
    """
    Find the interior cavity using flood-fill from outside.
    Returns the count of interior empty spaces.
    """
    # Create a copy to mark reachable empty spaces
    reachable = np.zeros_like(grid)
    
    # Start flood fill from all outer boundary empty positions
    queue = deque()
    
    # Add all empty positions on the boundaries
    for x in range(15):
        for y in range(15):
            for z in range(9):
                # Check if position is on boundary and empty
                on_boundary = (x == 0 or x == 14 or y == 0 or y == 14 or z == 0 or z == 8)
                if on_boundary and grid[x, y, z] == 0:
                    queue.append((x, y, z))
                    reachable[x, y, z] = 1
    
    # Flood fill
    directions = [
        (-1, 0, 0), (1, 0, 0),  # X axis
        (0, -1, 0), (0, 1, 0),  # Y axis
        (0, 0, -1), (0, 0, 1)   # Z axis
    ]
    
    while queue:
        x, y, z = queue.popleft()
        
        for dx, dy, dz in directions:
            nx, ny, nz = x + dx, y + dy, z + dz
            
            # Check bounds
            if 0 <= nx < 15 and 0 <= ny < 15 and 0 <= nz < 9:
                # If empty and not yet marked as reachable
                if grid[nx, ny, nz] == 0 and reachable[nx, ny, nz] == 0:
                    reachable[nx, ny, nz] = 1
                    queue.append((nx, ny, nz))
    
    # Interior empty spaces = empty spaces that are NOT reachable from outside
    interior_empty = np.where((grid == 0) & (reachable == 0))
    interior_count = len(interior_empty[0])
    
    return interior_count, interior_empty

def main():
    """Main function to solve all three questions."""
    n, hex_values = parse_lego_file('ajandek.txt')
    print(f"Total bricks in file: {n}")
    
    # Question 1: Count red bricks
    brick_stats = analyze_bricks(hex_values)
    
    print(f"ANSWER 1: {brick_stats['red']}")
    
    # Question 2 & 3: Find interior cavity (which also reveals captain's age)
    grid = build_3d_grid(brick_stats['positions'])
    interior_count, interior_empty = find_interior_cavity(grid)
    
    total_volume = 15 * 15 * 9
    filled_positions = np.sum(grid)
    all_empty = total_volume - filled_positions
    exterior_empty = all_empty - interior_count

    print(f"ANSWER 2: {interior_count}")

    return {
        'question1': brick_stats['red'],
        'question2': interior_count,
        'question3': interior_count
    }

main()

