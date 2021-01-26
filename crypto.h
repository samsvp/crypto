#pragma once

#include <string>
#include <map>

// saves in hash maps the letters and their positions
const int LOWER_BOUND = 'a';
const int UPPER_BOUND = 'z';
const int LOWER_A_VALUE = 'a';
const int ALPHABET_SIZE = UPPER_BOUND - LOWER_BOUND;
std::map<int, char> LETTER_MAP;
std::map<char, int> REVERSE_LETTER_MAP;

void create_letter_map();

std::map<char, int> get_caesar_letter_map(int offset);

// https://en.wikipedia.org/wiki/Caesar_cipher
std::string caesar(std::string text, int offset);

// https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher
std::string vigenere(std::string text, std::string keyword);

// https://en.wikipedia.org/wiki/Rail_fence_cipher
std::string rail_fence(std::string text, int key);

// https://en.wikipedia.org/wiki/XOR_cipher
std::string xor(std::string text, char key);