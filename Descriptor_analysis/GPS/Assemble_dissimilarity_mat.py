import pickle
from sklearn.manifold import MDS
import matplotlib.pyplot as plt
import numpy as np


def myargwhere(l, value):
    """
    Returns indexes {i} in l where l[i] == value
    """
    return (np.array(l) == value).nonzero()[0]


def scatter(x, y):
    """
    Plots a labeled scatter plot in matplotlib
    """
    _, ax = plt.subplots(figsize=(1,1))
    ax.scatter(x, y)
    ax.legend()
    plt.show()


n = 234
m = 1

dists = [None] * n
# compute distance matrix
for i in range(n):
    with open("./pickles/dists_{}.pickle".format(i), 'rb') as distF:
        dists[i] = pickle.load(distF)

# print('test')

for i in range(n):
    for j in range(i):
        dists[j][i] = dists[i][j]

embedder = MDS(dissimilarity='precomputed')
embedding = embedder.fit_transform(dists)
scatter(embedding[:, 0], embedding[:, 1])
