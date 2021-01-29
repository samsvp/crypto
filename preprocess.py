"""
Code to preprocess a dataset to use it on Machine
Learning algorithms
"""

import os
import cryptoanalysis
from algorithms import cypher_types
from typing import Tuple, Dict, List


def get_files() -> Tuple[Dict[str, List[str]], Dict[str, List[str]]]:
    train = {folder : ["train/" + folder + "/" + mfile for mfile in os.listdir("train/" + folder)]
                             for folder in os.listdir("train") }
    val = {folder : ["val/" + folder + "/" + mfile for mfile in os.listdir("val/" + folder)]
                           for folder in os.listdir("val") }
    return train, val

def preprocess(text: str) -> str:
    """
    Remove special characters, numbers and pass text to lowercase
    """
    p_text = "".join(letter for letter in text.lower() if (letter.isalpha() or letter.isspace()))
    return p_text.encode('ascii', 'ignore').decode('utf-8')

def read_file(file_name: str) -> str:
    with open(file_name) as f:
        data = f.read()
    return data

def write_file(data: str, filename: str) -> str:
    with open(filename, "w+") as f:
        f.write(data)

def create_test_set(train: bool) -> Tuple[List[float], List[int]]:
    train_files, val_files = get_files()
    X = []
    Y = []
    files = train_files if train else val_files
    for c_type in files:
        for file_name in files[c_type]:
            if "decrypted" in file_name: continue    
            text = preprocess(read_file(file_name))
            try:
                ioc = cryptoanalysis.index_of_coincidence(text)
                freq = cryptoanalysis.letter_frequency(text)
                freq_list = [freq[letter] for letter in freq]
            except ZeroDivisionError:
                continue
            X.append([*freq_list, ioc])
            Y.append(cypher_types[c_type])
    return X, Y

def save_data(X: List[List[float]], Y: List[int], file_name: str):
    with open(file_name, "w") as f:
        f.write(f"{X},{Y}")

def main():
    X, Y = create_test_set(True)
    save_data(X, Y, "train.txt")
    X, Y = create_test_set(False)
    save_data(X, Y, "val.txt")

if __name__ == "__main__":
    main()
