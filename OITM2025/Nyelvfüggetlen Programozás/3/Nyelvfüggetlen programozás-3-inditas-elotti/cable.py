from collections import deque, Counter

def find_single_point_of_failure(file_path, endpoints_to_check, central_box):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    num_cables = int(lines[0].strip())
    
    # Build adjacency graph: box -> [(neighbor_box, cable_num)]
    graph = {}
    box_connections = {}
    
    for i in range(1, num_cables + 1):
        parts = lines[i].strip().split()
        cable_num = parts[0]
        box_a = parts[1]
        box_b = parts[2]
        
        if box_a not in graph:
            graph[box_a] = []
        if box_b not in graph:
            graph[box_b] = []
        
        graph[box_a].append((box_b, cable_num))
        graph[box_b].append((box_a, cable_num))
        
        box_connections[box_a] = box_connections.get(box_a, 0) + 1
        box_connections[box_b] = box_connections.get(box_b, 0) + 1
    
    all_endpoints = [box for box, count in box_connections.items() if count == 1]
    
    print(f"Total endpoints found: {len(all_endpoints)}")
    
    # BFS
    def find_path(start, end):
        if start not in graph or end not in graph:
            return None
        
        queue = deque([(start, [start], [])])  # (current_box, path_boxes, path_cables)
        visited = {start}
        while queue:
            current, path_boxes, path_cables = queue.popleft()
            if current == end:
                return path_boxes, path_cables
            for neighbor, cable_num in graph.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path_boxes + [neighbor], path_cables + [cable_num]))
        
        return None
    
    for box in endpoints_to_check:
        count = box_connections.get(box, 0)
        is_endpoint = count == 1
        status = "ENDPOINT" if is_endpoint else f"NOT ENDPOINT (has {count} connections)"
        print(f"Box {box}: {status}")
      
    powered_endpoints = []
    unpowered_endpoints = []
    all_powered_routes = []
    
    for endpoint in all_endpoints:
        result = find_path(central_box, endpoint)
        if result:
            powered_endpoints.append(endpoint)
            path_boxes, path_cables = result
            all_powered_routes.append(set(path_cables))
        else:
            unpowered_endpoints.append(endpoint)
    
    print(f"Endpoints WITH power from {central_box}: {len(powered_endpoints)}")
    print(f"Endpoints WITHOUT power from {central_box}: {len(unpowered_endpoints)}")
    
    if unpowered_endpoints:
        print(f"\nEndpoints without power: {unpowered_endpoints}")
    
    specified_set = set(endpoints_to_check)
    unpowered_set = set(unpowered_endpoints)
    
    if specified_set == unpowered_set:
        print("CONFIRMED: The specified 4 endpoints are EXACTLY the ones without power!")
    else:
        print("MISMATCH:")
        only_specified = specified_set - unpowered_set
        only_unpowered = unpowered_set - specified_set
        if only_specified:
            print(f"  Specified but HAVE power: {only_specified}")
        if only_unpowered:
            print(f"  Unpowered but NOT specified: {only_unpowered}")
     
    target_routes = {}
    target_cables_in_routes = []
    
    for endpoint in endpoints_to_check:
        result = find_path(central_box, endpoint)
        target_routes[endpoint] = result
        
        print(f"\nRoute to endpoint {endpoint}:")
        if result:
            path_boxes, path_cables = result
            target_cables_in_routes.append(set(path_cables))
            print(f"Path: {len(path_cables)} cables")
            print(f"Boxes: {' → '.join(path_boxes[:5])} ... {' → '.join(path_boxes[-3:])}")
            print(f"Cables: {' → '.join(path_cables)}")
        else:
            print(f"NO ROUTE FOUND")
    

    if len(target_cables_in_routes) == len(endpoints_to_check):
        common_to_targets = target_cables_in_routes[0]
        for cable_set in target_cables_in_routes[1:]:
            common_to_targets = common_to_targets.intersection(cable_set)
        
        cables_only_for_targets = set(common_to_targets)
        
        for cable in common_to_targets:
            appears_in_other = False
            for i, endpoint in enumerate(powered_endpoints):
                if endpoint not in endpoints_to_check:
                    if cable in all_powered_routes[i]:
                        appears_in_other = True
                        break
            
            if appears_in_other:
                cables_only_for_targets.discard(cable)
        
        print(f"\nCables common to ALL 4 target endpoints: {len(common_to_targets)}")
        print(f"Cables that affect ONLY these 4 endpoints: {len(cables_only_for_targets)}")
        
        if cables_only_for_targets:
            print(f"Cable(s) that affect ONLY the 4 specified endpoints:")
            for cable in sorted(cables_only_for_targets):
                print(f"→ Cable {cable}")
                for i in range(1, num_cables + 1):
                    parts = lines[i].strip().split()
                    if parts[0] == cable:
                        print(f"Connects: {parts[1]} ←→ {parts[2]}")
                        break
            
            if len(cables_only_for_targets) == 1:
                cable_id = list(cables_only_for_targets)[0]
                print(f"\nIf cable {cable_id} fails, ONLY these 4 endpoints lose power!")
                print(f"All other {len(powered_endpoints) - 4} powered endpoints remain unaffected.")
        else:
            print(f"\n✓ No unique single point of failure found.")
            print(f"  All common cables also affect other endpoints.")
            
            print(f"\n   Cables common to target routes but also used by others:")
            for cable in sorted(common_to_targets):
                count = sum(1 for route in all_powered_routes if cable in route)
                print(f"   Cable {cable}: used by {count}/{len(powered_endpoints)} powered endpoints")
    
    return target_routes, cables_only_for_targets if len(target_cables_in_routes) == len(endpoints_to_check) else set()

def find_redundant_cables(file_path, central_box):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    num_cables = int(lines[0].strip())
    graph = {}
    box_connections = {}
    all_cables = {}  # cable_num: (box_a, box_b)
    
    for i in range(1, num_cables + 1):
        parts = lines[i].strip().split()
        cable_num = parts[0]
        box_a = parts[1]
        box_b = parts[2]
        
        all_cables[cable_num] = (box_a, box_b)
        
        if box_a not in graph:
            graph[box_a] = []
        if box_b not in graph:
            graph[box_b] = []
        
        graph[box_a].append((box_b, cable_num))
        graph[box_b].append((box_a, cable_num))
        
        box_connections[box_a] = box_connections.get(box_a, 0) + 1
        box_connections[box_b] = box_connections.get(box_b, 0) + 1
    
    all_endpoints = [box for box, count in box_connections.items() if count == 1]
    
    def bfs_distances(start, exclude_cable=None):
        distances = {start: 0}
        queue = deque([start])
        
        while queue:
            current = queue.popleft()
            current_dist = distances[current]
            for neighbor, cable_num in graph.get(current, []):
                if exclude_cable and cable_num == exclude_cable:
                    continue
                if neighbor not in distances:
                    distances[neighbor] = current_dist + 1
                    queue.append(neighbor)
        
        return distances
    
    baseline_distances = bfs_distances(central_box)
    redundant_cables = []
    
    cable_count = 0
    for cable_num, (box_a, box_b) in all_cables.items():
        cable_count += 1
        distances_without = bfs_distances(central_box, exclude_cable=cable_num)
        
        is_redundant = True
        affected_endpoints = []
        
        for endpoint in all_endpoints:
            baseline_dist = baseline_distances.get(endpoint)
            new_dist = distances_without.get(endpoint)
            
            if baseline_dist != new_dist:
                is_redundant = False
                if baseline_dist is not None and (new_dist is None or new_dist > baseline_dist):
                    affected_endpoints.append(endpoint)
        
        if is_redundant:
            redundant_cables.append({
                'cable': cable_num,
                'connects': (box_a, box_b),
                'affected': 0
            })
        elif affected_endpoints:
            pass
    
    if redundant_cables:
        lowest_cable = min(redundant_cables, key=lambda x: int(x['cable']))
        
        print(f"Cable {lowest_cable['cable']} (lowest number)")
        print(f"Connects: {lowest_cable['connects'][0]} ←→ {lowest_cable['connects'][1]}")
    else:
        print("No redundant cables found in the network.")
        print("All cables are critical for maintaining shortest paths.")
    
    return redundant_cables

endpoints_to_check = ['9526285', '1064470', '5702189', '4341735']
central_box = '1206792'
routes, common_cables = find_single_point_of_failure('altalanos/grid.txt', endpoints_to_check, central_box)
redundant_cables = find_redundant_cables('altalanos/grid.txt', central_box)
