"""
Conjunction of functions to make basic cryptoanalysis on 
a given text
"""

# %%
from typing import Dict

alphabet = "abcdefghijklmnopqrstuvwxyz"

def letter_count(text: str) -> Dict[str, int]:
    """
    Returns the number of times each letter in the alphabet has appeared
    in "text"
    """
    count = {letter : text.count(letter) for letter in alphabet}
    return count

def letter_frequency(text: str) -> Dict[str, float]:
    """
    Returns the frequency in which each letter appears in "text"
    """
    text_length = len(text)
    frequency = {letter : text.count(letter) / text_length for letter in alphabet}
    return frequency
    
def index_of_coincidence(text: str) -> float:
    """
    Returns the index of coincidence of "text"
    """
    N = len(text)
    F = letter_count(text)
    ioc = sum((F[i] * (F[i] - 1) for i in F)) / (N * (N - 1))
    return ioc

