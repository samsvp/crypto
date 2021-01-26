#include "crypto.h"
#include <algorithm>
#include <vector>
#include <string>
#include <fstream>
#include <iostream>
#include <sstream>
#include <cctype>
#include <cstdlib>
#include <stack>
#include <omp.h>
#include <random>
#include <filesystem>

namespace fs = std::filesystem;

using u32 = uint_least32_t;
using engine = std::mt19937;

const int test_size = 1000;
const int train_size = 10000;

void create_letter_map()
{
	for (int i = 0; i <= ALPHABET_SIZE; i++)
	{
		char letter = LOWER_BOUND + i;
		LETTER_MAP[i] = letter;
		REVERSE_LETTER_MAP[letter] = i;
	}
}

std::map<char, int> get_caesar_letter_map(int offset)
{
	std::map<char, int> encrypted_letter_map;
	for (int i = 0; i <= ALPHABET_SIZE; i++) // 26 letters in the alphabet
	{
		char letter = LOWER_BOUND + i;
		int pos = i + offset;
		if (pos > ALPHABET_SIZE) pos -= ALPHABET_SIZE + 1;
		encrypted_letter_map[letter] = pos;
	}
	return encrypted_letter_map;
}

char caesar(char letter, int offset)
{
	if (letter == ' ') return letter;

	auto encrypted_letter_map = get_caesar_letter_map(offset);

	int idx = encrypted_letter_map[std::tolower(letter)];
	char encrypted = LETTER_MAP[idx];

	return encrypted;
}

std::string caesar(std::string text, int offset)
{
	auto encrypted_letter_map = get_caesar_letter_map(offset);

	std::string encrypted;
	for (auto& letter : text)
	{
		if (letter == ' ')
		{
			encrypted += letter;
			continue;
		}
		int idx = encrypted_letter_map[std::tolower(letter)];
		encrypted += LETTER_MAP[idx];
	}
	return encrypted;
}

std::string vigenere(std::string text, std::string keyword)
{
	auto get_offset = [](char c) -> int {
		return REVERSE_LETTER_MAP[std::tolower(c)] - LOWER_A_VALUE + LOWER_BOUND + 1;
	};

	std::string encrypted = text;
	int letter_pos = 0;
	for (char& letter : keyword)
	{
		int offset = get_offset(letter);
		for (int i = letter_pos; i < encrypted.length(); i += keyword.length())
		{
			encrypted[i] = caesar(encrypted[i], get_offset(letter));
		}
		letter_pos++;
	}
	return encrypted;
}

std::string rail_fence(std::string text, int key)
{
	std::string encrypted;

	std::vector<std::string> rows(key);
	int spacing = (2 * key - 2);
	// Make the zig-zag
	for (int i = 0; i < text.length() / key; i++)
	{
		int offset = spacing * i;
		for (int j = offset; (j < offset + spacing / 2) && (j < text.length()); j++)
		{
			rows[j - offset] += text[j];
		}
		for (int j = offset + spacing / 2; (j < offset + spacing) && (j < text.length()); j++)
		{
			rows[spacing - (j - offset)] += text[j];
		}
	}

	for (int i = 0; i < key; i++) encrypted += rows[i];

	return encrypted;
}

std::string xor(std::string text, char key)
{
	std::string encrypted;
	for (auto& letter : text) encrypted += (letter ^ key);
	return encrypted;
}


std::string absolute_path(std::string relative_path)
{
	std::string file_path = __FILE__;
	std::string dir_path = file_path.substr(0, file_path.rfind("\\"));
	return dir_path + "\\" + relative_path;
}

/// returns a vector containing the text of all boo9ks inside the data folder.
std::vector<std::string> read_data()
{
	std::string path = absolute_path("data");
	std::vector<std::string> files;
	for (const auto & entry : fs::directory_iterator(path))
	{
		files.push_back(entry.path().string());
	}
	return files;
}

/// returns the content a plain text file in a string.
std::string read_file(std::string filename)
{
	std::ifstream t(filename);
	std::stringstream buffer;
	buffer << t.rdbuf();
	return buffer.str();
}

void write_file(std::string _name, std::vector<std::string> content, bool relative_path = true)
{
	std::string name = relative_path ? absolute_path(_name) : _name;
	std::ofstream myfile;
	myfile.open(name);
	for (std::string& c : content)
		myfile << c << std::endl;
	myfile.close();
}

void write_file(std::string _name, std::string content, bool relative_path = true)
{
	std::vector<std::string> v{ content };
	write_file(_name, v, relative_path);
}

/// Transforms a vector of strings into a single string
std::string vec_to_string(std::vector<std::string> v)
{
	std::string s;
	for (std::string& vs : v) s += vs;
	return s;
}

std::string remove_special_chars(std::string _s)
{
	std::string s = _s;
	s.resize(std::remove_if(
		s.begin(), s.end(), [](unsigned char x) {return !std::isalnum(x) && !std::isspace(x); }) - s.begin()
	);
	return s;
}

int get_random_number(int min, int max)
{
	static std::random_device os_seed;
	static const u32 seed = os_seed();

	static engine generator(seed);
	std::uniform_int_distribution< u32 > distribute(min, max);

	return distribute(generator);
}

// Generates a string of random chars with length between 3 anb 30
std::string get_random_string()
{
	static std::string alphabet = "abcdefghijklmnopqrstuwxyz";
	std::string s;
	int length = get_random_number(3, 30);
	for (int i = 0; i <= length; i++)
	{
		s += alphabet[get_random_number(0, alphabet.size() - 1)];
	}
	return s;
}

std::vector<std::string> get_paragraphs(std::string text)
{
	std::vector<std::string> paragraphs;
	std::string paragraph;

	std::istringstream text_stream(text);
	std::string line;
	while (std::getline(text_stream, line))
	{
		paragraph += line;
		if (!line.empty()) continue;
		paragraphs.push_back(paragraph);
		paragraph = "";
	}
	paragraphs.push_back(paragraph);
	return paragraphs;
}

/// Gets a slice of size n from the given "paragraphs" variable starting at a random index.
std::vector<std::string> get_random_paragraphs(std::vector<std::string> paragraphs, int n)
{
	int size = paragraphs.size();

	int start = get_random_number(0, size - n - 1);
	int end = start + n;

	std::vector<std::string> random_paragraphs(
		paragraphs.begin() + start,
		paragraphs.begin() + end
	);

	return random_paragraphs;
}

void create_training_set(int size, bool training = true)
{
	std::string folder = training ? "train\\" : "val\\";

	std::vector<std::string> file_names = read_data();

	std::vector<std::vector<std::string>> books;
	for (auto& f : file_names)
	{
		std::string book = read_file(f);
		books.push_back(get_paragraphs(book));
	}

	for (int i = 0; i < size; i++)
	{
		std::vector<std::string> book = books[get_random_number(0, books.size() - 1)];
		int n = get_random_number(3, 20);
		std::vector<std::string> paragraphs = get_random_paragraphs(book, n);

		// choose which algorithm to encrypt the text
		int algorithm = get_random_number(0, 3);

		std::string algorithm_name;
		std::string paragraphs_string = remove_special_chars(vec_to_string(paragraphs));
		std::string encrypted_string;
		switch (algorithm)
		{
		case 0:
			encrypted_string = caesar(paragraphs_string, get_random_number(1, 25)); // from B to Z
			algorithm_name = "caesar\\";
			break;
		case 1:
			encrypted_string = vigenere(paragraphs_string, get_random_string());
			algorithm_name = "vigenere\\";
			break;
		case 2:
			encrypted_string = rail_fence(paragraphs_string, get_random_number(2, 8));
			algorithm_name = "rail_fence\\";
			break;
		case 3:
			encrypted_string = xor (paragraphs_string, get_random_number(0, 127)); // all char range
			algorithm_name = "xor\\";
			break;
		default:
			throw;
			break;
		}

		write_file(folder + algorithm_name + std::to_string(i) + "_encrypted.txt", encrypted_string);
		write_file(folder + algorithm_name + std::to_string(i) + "_decrypted.txt", paragraphs_string);

		std::cout << i << std::endl;
	}
}

int main()
{
	create_letter_map();
	create_training_set(2000);
	create_training_set(500, false);
	return 0;
}