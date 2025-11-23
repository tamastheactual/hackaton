from collections import Counter

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


def score_hungarian(text):
    hungarian_freq = {
        'a': 8.5, 'e': 9.5, 'i': 3.5, 'o': 3.5, 't': 6.0, 'n': 5.0, 
        'l': 4.5, 's': 5.0, 'k': 4.0, 'r': 4.0, 'm': 3.0, 'z': 3.0,
        'g': 2.5, 'd': 2.5, 'v': 2.0, 'b': 2.0, 'y': 2.0, 'p': 1.5
    }
    
    common_bigrams = ['az', 'en', 'er', 'es', 'et', 'ez', 'le', 'te', 'an', 'el', 'is', 'sz']
    common_trigrams = ['ett', 'egy', 'sze', 'nek', 'ent', 'tet', 'van', 'hoz']
    common_words = ['egy', 'van', 'nem', 'azt', 'ezt', 'csak', 'amit', 'ahol', 'mint', 'hogy']
    
    text_lower = text.lower()
    letters_only = ''.join(c for c in text_lower if c.isalpha())
    
    if len(letters_only) == 0:
        return 0
    
    score = 0
    
    letter_counts = Counter(letters_only)
    for letter, expected_freq in hungarian_freq.items():
        actual_freq = (letter_counts.get(letter, 0) / len(letters_only)) * 100
        score -= abs(actual_freq - expected_freq)
    
    for bigram in common_bigrams:
        score += text_lower.count(bigram) * 5
    
    for trigram in common_trigrams:
        score += text_lower.count(trigram) * 10
    
    words = text_lower.split()
    for word in common_words:
        score += words.count(word) * 20
    
    for i in range(len(letters_only) - 2):
        if letters_only[i] == letters_only[i+1] == letters_only[i+2]:
            score -= 10
    
    return score

with open('kodolt_uzenet.txt', 'r', encoding='utf-8') as f:
    encoded_text = f.read().strip()

common_hungarian_codes = [
    'kulcsok', 'titokos', 'rejtelm', 'uzenet', 'valami', 
    'semmi', 'minden', 'nagyon', 'szerint', 'egeszen',
    'allando', 'erdekes', 'fontos', 'kerulet', 'lancos'
]

best_score = float('-inf')
best_code = None
best_decoded = None

for code_word in common_hungarian_codes:
    if len(code_word) == 7:
        decoded = esperente_decode(encoded_text, code_word)
        score = score_hungarian(decoded)
        
        if score > best_score:
            best_score = score
            best_code = code_word
            best_decoded = decoded
            print(f"New best: {code_word} (score: {score:.2f})")
            print(f"First 100 chars: {decoded[:100]}")

print(f"\nDecoded text:\n{best_decoded}")
