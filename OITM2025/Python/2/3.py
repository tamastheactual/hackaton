def simulate_nanobots(filename, time_units):
    with open(filename, 'r') as f:
        data = f.read().strip()
        initial_state = [int(x) for x in data.split(',')]
    
    counts = [0] * 9
    for timer in initial_state:
        counts[timer] += 1
    
    for _ in range(time_units):
        new_counts = [0] * 9
        
        dividing = counts[0]
        new_counts[6] += dividing  # Parent resets to 6
        new_counts[8] += dividing  # Child starts at 8
        
        for timer in range(1, 9):
            new_counts[timer - 1] += counts[timer]
        
        counts = new_counts
    
    return sum(counts)

result = simulate_nanobots('nano_keverek.txt', 60)
print(result)
