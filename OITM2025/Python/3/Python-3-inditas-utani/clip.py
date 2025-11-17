import os
from collections import Counter, defaultdict
from transformers import pipeline
from PIL import Image
import warnings
warnings.filterwarnings("ignore")

classifier = pipeline("zero-shot-image-classification", model="openai/clip-vit-base-patch32")

prefix_to_label = {
    '003': 'speed limit', '005': 'speed limit', '007': 'speed limit',
    '030': 'bicycles only', '035': 'zebra crossing', '054': 'no stopping', '055': 'no entry restriction'
}

candidate_labels = ['speed limit', 'bicycles only', 'zebra crossing', 'no stopping', 'no entry restriction']

data_dir = 'altalanos/data/DATA'
image_files = sorted([f for f in os.listdir(data_dir) if f.endswith(('.png', '.jpg', '.jpeg'))])
confidence_threshold = 0.5

results = []
labeled_count = Counter()

for img_file in image_files:
    prefix = img_file[:3]
    ground_truth = prefix_to_label.get(prefix, 'unknown')
    image = Image.open(os.path.join(data_dir, img_file))
    predictions = classifier(image, candidate_labels=candidate_labels)
    top_prediction = predictions[0]
    predicted_label = top_prediction['label']
    confidence = top_prediction['score']
    assigned_label = predicted_label if confidence > confidence_threshold else None
    
    if assigned_label:
        labeled_count[assigned_label] += 1
    
    results.append({
        'ground_truth': ground_truth,
        'predicted': predicted_label,
        'confidence': confidence,
        'assigned': assigned_label
    })

sorted_labels = sorted(labeled_count.items(), key=lambda x: x[1])
worst_class = sorted_labels[0][0] if sorted_labels else None

misclassifications = Counter()
misclassified_by_class = defaultdict(int)
correctly_classified_by_class = defaultdict(int)

for result in results:
    if result['ground_truth'] != 'unknown' and result['assigned'] is not None:
        if result['ground_truth'] != result['assigned']:
            misclassifications[(result['ground_truth'], result['assigned'])] += 1
            misclassified_by_class[result['ground_truth']] += 1
        else:
            correctly_classified_by_class[result['ground_truth']] += 1

always_correct_classes = []
for label in candidate_labels:
    total_labeled = len([r for r in results if r['ground_truth'] == label and r['assigned'] is not None])
    if total_labeled > 0 and misclassified_by_class.get(label, 0) == 0:
        always_correct_classes.append(label)

worst_misclassified = max(misclassified_by_class.items(), key=lambda x: x[1])[0] if misclassified_by_class else None

print(f"Least labeled class: {worst_class}")
print(f"Most wrongly categorized class: {worst_misclassified}")
print(f"Always correctly classified: {', '.join(always_correct_classes)}")
