# %%
from typing import Dict

LOWER_BOUND = ord('a')
UPPER_BOUND = ord('z')
LOWER_A_VALUE = ord('a')
ALPHABET_SIZE = UPPER_BOUND - LOWER_BOUND
LETTER_MAP = {}
REVERSE_LETTER_MAP = {}

cypher_types = {
    "caesar": 0, "vigenere": 1,
    "rail_fence": 2, "xor": 3
}

reverse_cypher_types = {
    0: "caesar/", 1: "vigenere/",
    2: "rail_fence/", 3: "xor/"
}

for i in range(ALPHABET_SIZE + 1):
    letter = chr(LOWER_BOUND + i)
    LETTER_MAP[i] = letter
    REVERSE_LETTER_MAP[letter] = i


def get_caesar_letter_map(offset: int) -> Dict[str, int]:
	encrypted_letter_map = {}

	for i in range(ALPHABET_SIZE + 1):
		letter = chr(LOWER_BOUND + i)
		pos = i + offset
		if pos > ALPHABET_SIZE:
			pos -= ALPHABET_SIZE + 1
		encrypted_letter_map[letter] = pos

	return encrypted_letter_map


def caesar(text: str, offset: int) -> str:
    encrypted_letter_map = get_caesar_letter_map(offset)

    encrypted = ""
    for letter in text:
        if ((letter == ' ') or (letter == '\n')):
            encrypted += letter
            continue
        idx = encrypted_letter_map[letter.lower()]
        encrypted += LETTER_MAP[idx]

    return encrypted


def vigenere(text: str, keyword: str) -> str:
    get_offset = lambda c : \
        REVERSE_LETTER_MAP[c.lower()] - LOWER_A_VALUE + LOWER_BOUND + 1

    encrypted = [""] * len(text)
    letter_pos = 0
    # Could be optimized, but this is just to create the training
    # corpora anyway
    for letter in keyword:
        for i in range(letter_pos, len(encrypted), len(keyword)):
            encrypted[i] = caesar(text[i], get_offset(letter))
        letter_pos += 1
    return "".join(encrypted)


def rail_fence(text: str, key: int) -> str:
    rows = [""] * key
    spacing = (2 * key - 2)
    # Make the zig-zag
    for i in range(len(text) // key):
        offset = spacing * i
        for j in range(offset, min(offset + spacing // 2, len(text))):
            rows[j - offset] += text[j]
        for j in range(offset + spacing // 2, min(offset + spacing, len(text))): 
            rows[spacing - (j - offset)] += text[j]

    encrypted = "".join(rows)
    return encrypted


def xor(text: str, key: str) -> str:
    return "".join([chr(ord(letter) ^ ord(key)) for letter in text])
