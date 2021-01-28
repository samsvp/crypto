from typing import Dict

LOWER_BOUND = ord('a')
UPPER_BOUND = ord('z')
ALPHABET_SIZE = UPPER_BOUND - LOWER_BOUND
LETTER_MAP = {}
REVERSE_LETTER_MAP = {}


def create_letter_map():
    for i in range(ALPHABET_SIZE):
        letter = chr(LOWER_BOUND + i)
        LETTER_MAP[i] = letter
        REVERSE_LETTER_MAP[letter] = i


def get_caesar_letter_map(offset: int) -> Dict[str, int]:
	encrypted_letter_map = {}

	for i in range(ALPHABET_SIZE):
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
        if (letter == ' '):
            encrypted += letter
            continue
        idx = encrypted_letter_map[letter.lower()]
        encrypted += LETTER_MAP[idx]

    return encrypted


def vigenere(text: str, keyword: str) -> str:
    get_offset = lambda c : \
        REVERSE_LETTER_MAP[c.lower()] - LOWER_A_VALUE + LOWER_BOUND + 1

    encrypted = text
    letter_pos = 0
    for letter in keyword:
        offset = get_offset(letter)
        for i in range(letter_pos, len(encrypted), len(keyword)):
            encrypted[i] = caesar(encrypted[i], get_offset(letter))
        letter_pos += 1
    return encrypted


def rail_fence(text: str, key: int) -> str:
    encrypted = ""

    rows = [""] * key
    spacing = (2 * key - 2)
    # Make the zig-zag
    for i in range(len(text) // key ):
        offset = spacing * i
        for (int j=offset(j < offset + spacing / 2) & & (j < text.length()) j++)
        {
            rows[j - offset] += text[j]
        }
        for (int j=offset + spacing / 2 (j < offset + spacing) & & (j < text.length()) j++)
        {
            rows[spacing - (j - offset)] += text[j]
        }

    for (int i=0 i < key i++) encrypted += rows[i]

    return encrypted
}

std: : string cxor(std: : string text, char key)
{
    std:: string encrypted
    for (auto & letter: text) encrypted += (letter ^ key)
    return encrypted
}
