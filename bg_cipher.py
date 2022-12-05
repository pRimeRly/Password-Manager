DEFAULT_SHIFT_KEY = 3
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
            'z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


def encode(password):

    key = DEFAULT_SHIFT_KEY
    key = key % 26
    text = password[::-1]
    end_text = ""
    for char in text:
        if char in alphabet:
            position = alphabet.index(char)
            new_position = position + key
            end_text += alphabet[new_position]
        else:
            end_text += char
    return end_text


def decode(password):
    key = DEFAULT_SHIFT_KEY
    key = key % 26
    text = password[::-1]
    end_text = ""
    for char in text:
        if char in alphabet:
            position = alphabet.index(char)
            new_position = position - key
            end_text += alphabet[new_position]
        else:
            end_text += char
    return end_text


# Implement Encode function in save() function
# Implement Decode function in search_password() function
