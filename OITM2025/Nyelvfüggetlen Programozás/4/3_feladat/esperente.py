def esperente_encode(sentence, code):
    result = []
    code_index = 0
    for char in sentence:
        if char.isalpha():
            sentence_pos = ord(char.lower()) - ord('a')
            code_pos = ord(code[code_index % 7].lower()) - ord('a')
            encoded_pos = (sentence_pos + code_pos) % 26
            encoded_char = chr(encoded_pos + ord('a'))
            
            result.append(encoded_char)
            code_index += 1
        else:
            result.append(char)
    
    return ''.join(result)

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

def find_code(original, encoded):
    code_letters = []
    orig_idx = 0
    enc_idx = 0
    while orig_idx < len(original) and enc_idx < len(encoded):
        if original[orig_idx].isalpha() and encoded[enc_idx].isalpha():
            orig_pos = ord(original[orig_idx].lower()) - ord('a')
            enc_pos = ord(encoded[enc_idx].lower()) - ord('a')
            code_pos = (enc_pos - orig_pos) % 26
            code_letter = chr(code_pos + ord('a'))
            code_letters.append(code_letter)
            orig_idx += 1
            enc_idx += 1
        elif not original[orig_idx].isalpha():
            orig_idx += 1
        elif not encoded[enc_idx].isalpha():
            enc_idx += 1
    if len(code_letters) >= 7:
        code_word = ''.join(code_letters[:7])
        print(f"Code pattern: {code_letters[:14]}")
        return code_word
    
    return None

sentence = "kedvenc eledelem: cseresznye"
code = "tesztem"

print(f"Original: {sentence}")
print(f"Code: {code}")
encoded = esperente_encode(sentence, code)
print(f"Encoded: {encoded}")
decoded = esperente_decode(encoded, code)
print(f"Decoded: {decoded}")

sentence2 = "egy kedves teszt. nem felesleges."
code2 = "szellem"
encoded_text = "wfc vphhwr xpddf. fdq qppqkkirpw."

print(f"Original: {sentence2}")
print(f"Code: {code2}")
encoded2 = esperente_encode(sentence2, code2)
print(f"Encoded: {encoded2}")
print(f"Expected: {encoded_text}")

decoded2 = esperente_decode(encoded_text, code2)
print(f"Decoded: {decoded2}")
print(f"Expected: {sentence2}")

sentence_3 = "qkpvx pqprco, mizkkpid qqwzcvx? wliyxil rqhbcx yixgycv xhq zkjiw zqhkjrx."
encoded_3 = "merre lellek, tengerek mestere? szeszes nedvet felcser ede veled vedelne."

code_3 = find_code(sentence_3, encoded_3)

if code_3:
    decoded_3 = esperente_decode(encoded_3, code_3)
    print(f"Decoded: {decoded_3}")
    print(f"Original: {sentence_3}")
    print(f"Match: {decoded_3 == sentence_3}")
