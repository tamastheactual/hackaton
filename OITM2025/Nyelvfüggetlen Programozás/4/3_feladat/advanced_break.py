from collections import Counter
from itertools import product

def esperente_decode(encoded, code):
    result = []
    code_index = 0
    
    for char in encoded:
        if char.isalpha():
            encoded_pos = ord(char.lower()) - ord('a')
            code_pos = ord(code[code_index % 7].lower()) - ord('a')
            sentence_pos = (encoded_pos - code_pos) % 26
            decoded_char = chr(sentence_pos + ord('a'))
            result.append(decoded_char)
            code_index += 1
        else:
            result.append(char)
    
    return ''.join(result)


def analyze_position(encoded_text, position):
    letters = []
    idx = 0
    for char in encoded_text:
        if char.isalpha():
            if idx % 7 == position:
                letters.append(char.lower())
            idx += 1
    return Counter(letters)

with open('kodolt_uzenet.txt', 'r', encoding='utf-8') as f:
    encoded_text = f.read().strip()

hungarian_common = 'aetsnlrikzmogdvbpjyufhcw'
code_candidates = []

for pos in range(7):
    freq = analyze_position(encoded_text, pos)
    most_common = freq.most_common(3)
    print(f"Position {pos}: {most_common}")
    
    candidates_for_pos = []
    for encoded_letter, count in most_common[:2]:
        for target in ['a', 'e', 't']:
            encoded_pos = ord(encoded_letter) - ord('a')
            target_pos = ord(target) - ord('a')
            code_pos = (encoded_pos - target_pos) % 26
            code_letter = chr(code_pos + ord('a'))
            candidates_for_pos.append((code_letter, count))
    
    code_candidates.append(candidates_for_pos)

def score_text(text):
    text = text.lower()
    score = 0
    
    words = ['egy', 'van', 'nem', 'azt', 'amit', 'csak', 'mint', 'hogy', 'volt', 'meg']
    for word in words:
        score += text.count(' ' + word + ' ') * 50
        score += text.count(' ' + word + ',') * 50
        score += text.count(' ' + word + '.') * 50
    
    score += text.count('nak') * 10
    score += text.count('nek') * 10
    score += text.count('ban') * 10
    score += text.count('ben') * 10
    score += text.count('ett') * 10
    
    score += text.count('sz') * 5
    score += text.count('az') * 5
    score += text.count('el') * 5
    
    return score

best_score = float('-inf')
best_code = None
best_decoded = None

tested = 0
for combination in product(*[[(c, cnt) for c, cnt in pos[:2]] for pos in code_candidates]):
    code = ''.join([c for c, cnt in combination])
    decoded = esperente_decode(encoded_text, code)
    score = score_text(decoded)
    
    tested += 1
    
    if score > best_score:
        best_score = score
        best_code = code
        best_decoded = decoded
        print(f"Code: {code} | Score: {score:.1f}")
        print(f"Sample: {decoded[:100]}...")
        print()

print(f"\nDecoded message:\n{best_decoded}")
