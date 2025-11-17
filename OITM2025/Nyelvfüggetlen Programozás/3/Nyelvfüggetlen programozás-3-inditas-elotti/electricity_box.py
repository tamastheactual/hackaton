def count_unique_boxes(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    num_cables = int(lines[0].strip())
    boxes = set()
    for i in range(1, num_cables + 1):
        parts = lines[i].strip().split()
        box_a = parts[1]
        box_b = parts[2]
        boxes.add(box_a)
        boxes.add(box_b)
    
    return len(boxes)

result = count_unique_boxes('altalanos/grid.txt')
print(result)