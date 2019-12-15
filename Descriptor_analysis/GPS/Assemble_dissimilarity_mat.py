import pickle
from sklearn.manifold import MDS
import matplotlib.pyplot as plt
import numpy as np
import os
import glob


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

def scatter_annotated(x, y, labels):
    """
    Plots a labeled scatter plot in matplotlib
    """
    _, ax = plt.subplots(figsize=(10,10))
    for g in range(len(np.unique(labels))):
        label_i = np.unique(labels)[g]
        i = myargwhere(labels, label_i)
        ax.scatter(x[i], y[i], label=label_i)
    ax.legend()
    plt.show()

def name(filename, eigs=False):
    """
    Returns shape name from a filepath
    """
    if eigs:
        return os.path.split(filename)[1].split('.')[0]
    else:
        return os.path.split(filename)[1][:-4].split('.')[0]


n = 212
m = 1
embeds_path = './results'

# embeds = glob.glob(embeds_path + '/*.txt')

# Split filename lists by descriptor
# embeds_gps = []
# embeds_shapedna = []
# for i in embeds:
#     if 'shapeDNA' in i:
#         embeds_shapedna.append(i)
#     else:
#         embeds_gps.append(i)

y_full = []
y_mid = []
y_simple = []
names = ['./results/camel-gallop-10.obj.20.GPS.txt',
         './results/face-02-cry.obj.20.GPS.txt',
         './results/elephant-gallop-41.obj.20.GPS.txt',
         './results/elephant-gallop-06.obj.20.GPS.txt',
         './results/elephant-gallop-15.obj.20.GPS.txt',
         './results/horse-collapose-02.obj.20.GPS.txt',
         './results/elephant-09.obj.20.GPS.txt',
         './results/elephant-gallop-45.obj.20.GPS.txt',
         './results/camel-collapse-39.obj.20.GPS.txt',
         './results/horse-gallop-41.obj.20.GPS.txt',
         './results/camel-collapse-28.obj.20.GPS.txt',
         './results/camel-gallop-42.obj.20.GPS.txt',
         './results/camel-collapse-47.obj.20.GPS.txt',
         './results/horse-collapose-52.obj.20.GPS.txt',
         './results/head-07-sad.obj.20.GPS.txt',
         './results/horse-collapose-04.obj.20.GPS.txt',
         './results/horse-gallop-43.obj.20.GPS.txt',
         './results/horse-collapose-39.obj.20.GPS.txt',
         './results/camel-collapse-34.obj.20.GPS.txt',
         './results/camel-gallop-20.obj.20.GPS.txt',
         './results/horse-collapose-06.obj.20.GPS.txt',
         './results/elephant-gallop-39.obj.20.GPS.txt',
         './results/horse-07.obj.20.GPS.txt',
         './results/elephant-gallop-43.obj.20.GPS.txt',
         './results/elephant-gallop-36.obj.20.GPS.txt',
         './results/elephant-03.obj.20.GPS.txt',
         './results/elephant-gallop-28.obj.20.GPS.txt',
         './results/face-04-grin.obj.20.GPS.txt',
         './results/camel-gallop-14.obj.20.GPS.txt',
         './results/elephant-gallop-27.obj.20.GPS.txt',
         './results/camel-collapse-17.obj.20.GPS.txt',
         './results/elephant-gallop-35.obj.20.GPS.txt',
         './results/camel-collapse-08.obj.20.GPS.txt',
         './results/horse-collapose-30.obj.20.GPS.txt',
         './results/elephant-gallop-04.obj.20.GPS.txt',
         './results/camel-collapse-27.obj.20.GPS.txt',
         './results/camel-gallop-32.obj.20.GPS.txt',
         './results/camel-collapse-11.obj.20.GPS.txt',
         './results/camel-collapse-10.obj.20.GPS.txt',
         './results/horse-collapose-reference.obj.20.GPS.txt',
         './results/elephant-gallop-07.obj.20.GPS.txt',
         './results/camel-gallop-39.obj.20.GPS.txt',
         './results/camel-collapse-24.obj.20.GPS.txt',
         './results/horse-collapose-47.obj.20.GPS.txt',
         './results/horse-collapose-34.obj.20.GPS.txt',
         './results/camel-collapse-25.obj.20.GPS.txt',
         './results/elephant-gallop-34.obj.20.GPS.txt',
         './results/horse-04.obj.20.GPS.txt',
         './results/elephant-gallop-22.obj.20.GPS.txt',
         './results/camel-collapse-40.obj.20.GPS.txt',
         './results/camel-collapse-31.obj.20.GPS.txt',
         './results/cat-08.obj.20.GPS.txt',
         './results/elephant-gallop-48.obj.20.GPS.txt',
         './results/face-08-smile.obj.20.GPS.txt',
         './results/horse-collapose-43.obj.20.GPS.txt',
         './results/elephant-gallop-20.obj.20.GPS.txt',
         './results/camel-collapse-48.obj.20.GPS.txt',
         './results/horse-gallop-29.obj.20.GPS.txt',
         './results/camel-collapse-16.obj.20.GPS.txt',
         './results/lion-08.obj.20.GPS.txt',
         './results/horse-gallop-20.obj.20.GPS.txt',
         './results/horse-collapose-29.obj.20.GPS.txt',
         './results/head-09-surprise.obj.20.GPS.txt',
         './results/horse-05.obj.20.GPS.txt',
         './results/lion-06.obj.20.GPS.txt',
         './results/elephant-10.obj.20.GPS.txt',
         './results/camel-gallop-08.obj.20.GPS.txt',
         './results/elephant-gallop-09.obj.20.GPS.txt',
         './results/horse-gallop-19.obj.20.GPS.txt',
         './results/cat-06.obj.20.GPS.txt',
         './results/camel-collapse-32.obj.20.GPS.txt',
         './results/elephant-gallop-23.obj.20.GPS.txt',
         './results/horse-collapose-16.obj.20.GPS.txt',
         './results/elephant-gallop-08.obj.20.GPS.txt',
         './results/camel-06.obj.20.GPS.txt',
         './results/horse-gallop-08.obj.20.GPS.txt',
         './results/horse-gallop-13.obj.20.GPS.txt',
         './results/elephant-gallop-44.obj.20.GPS.txt',
         './results/camel-gallop-03.obj.20.GPS.txt',
         './results/face-01-anger.obj.20.GPS.txt',
         './results/horse-collapose-48.obj.20.GPS.txt',
         './results/elephant-gallop-24.obj.20.GPS.txt',
         './results/horse-gallop-11.obj.20.GPS.txt',
         './results/camel-collapse-01.obj.15.GPS.txt',
         './results/elephant-gallop-reference.obj.20.GPS.txt',
         './results/face-09-surprise.obj.20.GPS.txt',
         './results/horse-collapose-25.obj.20.GPS.txt',
         './results/camel-gallop-23.obj.20.GPS.txt',
         './results/camel-collapse-38.obj.20.GPS.txt',
         './results/head-03-fury.obj.20.GPS.txt',
         './results/head-reference.obj.20.GPS.txt',
         './results/camel-collapse-29.obj.20.GPS.txt',
         './results/elephant-gallop-19.obj.20.GPS.txt',
         './results/horse-collapose-36.obj.20.GPS.txt',
         './results/camel-collapse-50.obj.20.GPS.txt',
         './results/elephant-04.obj.20.GPS.txt',
         './results/lion-07.obj.20.GPS.txt',
         './results/camel-collapse-42.obj.20.GPS.txt',
         './results/horse-collapose-31.obj.20.GPS.txt',
         './results/horse-collapose-12.obj.20.GPS.txt',
         './results/horse-gallop-32.obj.20.GPS.txt',
         './results/elephant-gallop-42.obj.20.GPS.txt',
         './results/camel-collapse-13.obj.20.GPS.txt',
         './results/horse-collapose-37.obj.20.GPS.txt',
         './results/elephant-gallop-11.obj.20.GPS.txt',
         './results/camel-reference.obj.20.GPS.txt',
         './results/elephant-05.obj.20.GPS.txt',
         './results/camel-collapse-36.obj.20.GPS.txt',
         './results/camel-gallop-27.obj.20.GPS.txt',
         './results/elephant-gallop-03.obj.20.GPS.txt',
         './results/cat-09.obj.20.GPS.txt',
         './results/horse-collapose-35.obj.20.GPS.txt',
         './results/camel-collapse-26.obj.20.GPS.txt',
         './results/elephant-01.obj.20.GPS.txt',
         './results/camel-gallop-01.obj.20.GPS.txt',
         './results/elephant-gallop-17.obj.20.GPS.txt',
         './results/horse-collapose-10.obj.20.GPS.txt',
         './results/horse-gallop-05.obj.20.GPS.txt',
         './results/face-03-fury.obj.20.GPS.txt',
         './results/camel-collapse-01.obj.20.GPS.txt',
         './results/camel-gallop-25.obj.20.GPS.txt',
         './results/camel-gallop-34.obj.20.GPS.txt',
         './results/camel-collapse-45.obj.20.GPS.txt',
         './results/horse-collapose-53.obj.20.GPS.txt',
         './results/camel-gallop-30.obj.20.GPS.txt',
         './results/camel-gallop-06.obj.20.GPS.txt',
         './results/camel-collapse-03.obj.20.GPS.txt',
         './results/camel-gallop-12.obj.20.GPS.txt',
         './results/horse-collapose-13.obj.20.GPS.txt',
         './results/elephant-gallop-13.obj.20.GPS.txt',
         './results/elephant-gallop-05.obj.20.GPS.txt',
         './results/camel-collapse-09.obj.20.GPS.txt',
         './results/horse-collapose-01.obj.20.GPS.txt',
         './results/cat-reference.obj.20.GPS.txt',
         './results/elephant-gallop-26.obj.20.GPS.txt',
         './results/elephant-06.obj.20.GPS.txt',
         './results/camel-collapse-43.obj.20.GPS.txt',
         './results/camel-collapse-21.obj.20.GPS.txt',
         './results/horse-gallop-45.obj.20.GPS.txt',
         './results/head-08-smile.obj.20.GPS.txt',
         './results/horse-gallop-35.obj.20.GPS.txt',
         './results/camel-gallop-15.obj.20.GPS.txt',
         './results/elephant-reference.obj.20.GPS.txt',
         './results/horse-collapose-45.obj.20.GPS.txt',
         './results/elephant-gallop-21.obj.20.GPS.txt',
         './results/horse-collapose-46.obj.20.GPS.txt',
         './results/elephant-gallop-33.obj.20.GPS.txt',
         './results/horse-collapose-18.obj.20.GPS.txt',
         './results/camel-collapse-19.obj.20.GPS.txt',
         './results/camel-gallop-43.obj.20.GPS.txt',
         './results/camel-04.obj.20.GPS.txt',
         './results/horse-collapose-14.obj.20.GPS.txt',
         './results/camel-collapse-06.obj.20.GPS.txt',
         './results/cat-05.obj.20.GPS.txt',
         './results/camel-collapse-53.obj.20.GPS.txt',
         './results/camel-gallop-36.obj.20.GPS.txt',
         './results/elephant-gallop-32.obj.20.GPS.txt',
         './results/elephant-gallop-12.obj.20.GPS.txt',
         './results/elephant-gallop-31.obj.20.GPS.txt',
         './results/camel-collapse-04.obj.20.GPS.txt',
         './results/elephant-gallop-38.obj.20.GPS.txt',
         './results/camel-gallop-38.obj.20.GPS.txt',
         './results/elephant-02.obj.20.GPS.txt',
         './results/horse-collapose-19.obj.20.GPS.txt',
         './results/elephant-gallop-14.obj.20.GPS.txt',
         './results/elephant-gallop-37.obj.20.GPS.txt',
         './results/elephant-07.obj.20.GPS.txt',
         './results/horse-09.obj.20.GPS.txt',
         './results/camel-gallop-18.obj.20.GPS.txt',
         './results/elephant-gallop-02.obj.20.GPS.txt',
         './results/elephant-gallop-46.obj.20.GPS.txt',
         './results/head-04-grin.obj.20.GPS.txt',
         './results/camel-collapse-07.obj.20.GPS.txt',
         './results/horse-collapose-05.obj.20.GPS.txt',
         './results/elephant-gallop-29.obj.20.GPS.txt',
         './results/camel-gallop-17.obj.20.GPS.txt',
         './results/elephant-gallop-40.obj.20.GPS.txt',
         './results/horse-collapose-50.obj.20.GPS.txt',
         './results/horse-collapose-41.obj.20.GPS.txt',
         './results/camel-collapse-46.obj.20.GPS.txt',
         './results/camel-gallop-19.obj.20.GPS.txt',
         './results/camel-gallop-47.obj.20.GPS.txt',
         './results/horse-collapose-28.obj.20.GPS.txt',
         './results/horse-collapose-32.obj.20.GPS.txt',
         './results/horse-collapose-11.obj.20.GPS.txt',
         './results/horse-gallop-17.obj.20.GPS.txt',
         './results/camel-collapse-44.obj.20.GPS.txt',
         './results/elephant-gallop-18.obj.20.GPS.txt',
         './results/horse-gallop-37.obj.20.GPS.txt',
         './results/camel-collapse-14.obj.20.GPS.txt',
         './results/elephant-gallop-30.obj.20.GPS.txt',
         './results/face-05-laugh.obj.20.GPS.txt',
         './results/horse-collapose-51.obj.20.GPS.txt',
         './results/cat-01.obj.20.GPS.txt',
         './results/camel-gallop-37.obj.20.GPS.txt',
         './results/elephant-gallop-10.obj.20.GPS.txt',
         './results/camel-collapse-51.obj.20.GPS.txt',
         './results/horse-collapose-21.obj.20.GPS.txt',
         './results/horse-collapose-49.obj.20.GPS.txt',
         './results/camel-gallop-13.obj.20.GPS.txt',
         './results/camel-gallop-31.obj.20.GPS.txt',
         './results/elephant-gallop-47.obj.20.GPS.txt',
         './results/camel-collapse-reference.obj.20.GPS.txt',
         './results/horse-gallop-44.obj.20.GPS.txt',
         './results/camel-collapse-35.obj.20.GPS.txt']

int_table = str.maketrans(dict.fromkeys('0123456789'))
for meshname in names:
    y_full.append(meshname)
    y_simple.append(meshname.split('-')[0])
    y_mid.append(meshname.translate(int_table).strip('-').replace('-reference', '').split('--', 1)[0])



dists = [None] * n
# compute distance matrix
for i in range(n):
    with open("./pickles/dataset/dists_{}.pickle".format(i), 'rb') as distF:
        dists[i] = pickle.load(distF)

# print('test')

for i in range(n):
    for j in range(i):
        dists[j][i] = dists[i][j]

embedder = MDS(dissimilarity='precomputed')
embedding = embedder.fit_transform(dists)
scatter_annotated(embedding[:, 0], embedding[:, 1], y_simple)
