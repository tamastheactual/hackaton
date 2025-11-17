def find_endpoints(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    num_cables = int(lines[0].strip())
    box_connections = {}
    
    for i in range(1, num_cables + 1):
        parts = lines[i].strip().split()
        box_a = parts[1]
        box_b = parts[2]
        
        box_connections[box_a] = box_connections.get(box_a, 0) + 1
        box_connections[box_b] = box_connections.get(box_b, 0) + 1
    
    endpoints = [box for box, count in box_connections.items() if count == 1]
    
    return sorted(endpoints)

endpoints = find_endpoints('altalanos/grid.txt')
print(f"Number of endpoints: {len(endpoints)}")
print(f"Endpoints: {endpoints}")
