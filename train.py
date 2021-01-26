"""
Script to train a Random Forest Classifier to differentiate
between four different encription methods: the caesar cypher,
the vigenere cypher, rail_fence cypher and xor cypher
"""

#%%
import numpy as np
from typing import Tuple, List
from sklearn.ensemble import RandomForestClassifier

def read_set(train: bool) -> Tuple[List[float], List[int]]:
    """
    Returns the training/validation sets ready to be used
    in sklearn algorithms
    """
    _set = "train.txt" if train else "val.txt"
    with open(_set) as f:
        text = f.read()
    data = eval(text)
    X, Y = data
    return np.array(X), np.array(Y)

def train(X: np.ndarray, Y: np.ndarray) -> RandomForestClassifier:
    """
    Trains a Random Forest Classifier to detect the type of cypher
    used to encrypt the text
    """
    clf = RandomForestClassifier(random_state=0)
    clf.fit(X, Y)
    return clf

def validate(X: np.ndarray, Y: np.ndarray, clf: RandomForestClassifier) -> float:
    shape = X[0].shape[0]
    right = 0
    for i in range(len(X)):
        pred = clf.predict(X[i].reshape(-1, shape))
        if pred == Y[i]: right += 1
    return right, float(right)/len(X)


X, Y = read_set(True)
Xv, Yv = read_set(False)

clf = train(X, Y)
p = validate(Xv, Yv, clf)