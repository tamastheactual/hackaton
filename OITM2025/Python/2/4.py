def first_reaching_mass(filename, target_kg=12, mg_per_nanobot=10):
    """Find the first second when nanobot mass reaches target."""
    # Read input
    with open(filename, 'r') as f:
        data = f.read().strip()
        initial_state = [int(x) for x in data.split(',')]
    
    # Convert target mass to number of nanobots needed
    target_mg = target_kg * 1_000_000  # kg to mg
    total_needed = target_mg // mg_per_nanobot
    
    # Initialize counts by timer value
    counts = [0] * 9
    for timer in initial_state:
        counts[timer] += 1
    
    # Simulate until we reach target
    for t in range(1000):  # Max 1000 seconds
        if sum(counts) >= total_needed:
            return t
        
        # Simulate one time step
        new_counts = [0] * 9
        dividing = counts[0]
        new_counts[6] += dividing  # Parent resets to 6
        new_counts[8] += dividing  # Child starts at 8
        
        for timer in range(1, 9):
            new_counts[timer - 1] += counts[timer]
        
        counts = new_counts
    
    return -1  # Not reached

# Run
result = first_reaching_mass('nano_keverek.txt')
print(result)
