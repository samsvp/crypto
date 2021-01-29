"""
Generates a training and validation set from the books inside
the data folder. The data is composed of paragraphs chosen at
random from the books.
"""

import os
import random
import preprocess
from algorithms import *
from typing import List

test_size = 1000
train_size = 10000

def get_random_string(k: int) -> str:
    return ''.join(random.choices('abcdefghijklmnopqestuvwxyz', k=k))

def get_random_paragraphs(text: str) -> str:
    _paragraphs = text.split("\n")
    paragraphs = random.sample(_paragraphs, k=random.randint(3, 20))
    return "\n".join(paragraphs)

def get_file_names() -> List[str]:
    return [f for f in os.listdir("data")]

def create_training_set(n: int, training=True):
    root_folder = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/") + '/'
    folder = root_folder + "train/" if training else root_folder + "val/"

    files = get_file_names()
    books = [preprocess.read_file(f"{root_folder}data/{f}") for f in files]

    for i in range(n):
        book = random.choice(books)
        paragraphs = preprocess.preprocess(get_random_paragraphs(book))
        k = random.randint(0, 2)
        algorithm_name = reverse_cypher_types[k]

        if algorithm_name == "caesar/":
            encrypted = caesar(paragraphs, random.randint(1, 25))
        elif algorithm_name == "vigenere/":
            encrypted = vigenere(paragraphs, get_random_string(random.randint(3, 25)))
        elif algorithm_name == "rail_fence/":
            encrypted = rail_fence(paragraphs, random.randint(2, 8))
        elif algorithm_name == "xor/":
            encrypted = xor(paragraphs, chr(random.randint(ord('a'), ord('z'))))
        else:
            raise Exception("Algorithm not found")
    
        preprocess.write_file(encrypted, f"{folder}{algorithm_name}{i}_encrypted.txt")
        preprocess.write_file(paragraphs, f"{folder}{algorithm_name}{i}_decrypted.txt")

        print(f"{folder}{algorithm_name}{i}")

if __name__ == "__main__":
    create_training_set(train_size)
    create_training_set(test_size, False)