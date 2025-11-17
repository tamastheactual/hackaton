def last_second_before_limit(filename, limit_kg=100, mg_per_nanobot=10):
    """Find the last second when nanobot mass is still at or below limit."""
    with open(filename, 'r') as f:
        data = f.read().strip()
        initial_state = [int(x) for x in data.split(',')]
    
    limit_mg = limit_kg * 1_000_000
    max_allowed = limit_mg // mg_per_nanobot
    
    counts = [0] * 9
    for timer in initial_state:
        counts[timer] += 1
    
    last_valid_second = 0
    
    for t in range(1000):
        if sum(counts) <= max_allowed:
            last_valid_second = t
        else:
            return last_valid_second
        
        new_counts = [0] * 9
        dividing = counts[0]
        new_counts[6] += dividing
        new_counts[8] += dividing
        
        for timer in range(1, 9):
            new_counts[timer - 1] += counts[timer]
        
        counts = new_counts
    
    return last_valid_second

result = last_second_before_limit('nano_keverek.txt', 100)
print(result)
