import numpy as np
import matplotlib.pyplot as plt
import os
import glob
from tqdm import tqdm
from itertools import combinations
from scipy.spatial.distance import cdist
from scipy.stats import ks_2samp
import seaborn as sns
from sklearn.manifold import TSNE, MDS
from sklearn.decomposition import PCA
from sklearn.neighbors import KernelDensity
from sklearn.manifold import MDS
import pickle


# Seed for random sampling (Rustamov)
seed_ = 42

# Paths for embedding files and mesh files
embeds_path = './results_princeton/results'
shapes_path = './models'

# Number of histograms and sample proportion for each region (Rustamov)
m = 1
prop = 0.05

# Type of metric for computing distances
metric_ = 'euclidean'

def name(filename, eigs=False):
    """
    Returns shape name from a filepath
    """
    if eigs:
        return os.path.split(filename)[1].split('.')[0]
    else:
        return os.path.split(filename)[1][:-4].split('.')[0]

def missing(embeds, shapes):
    """
    """
    shapes_names = [name(i, eigs=False) for i in shapes]
    embeds_names = [name(i, eigs=True) for i in embeds]
    misses = list(set(shapes_names).symmetric_difference(set(embeds_names)))
    return sorted(misses)

def dim(filename):
    """
    Given an embedding filename, returns how many eigs were supposedly computed
    """
    return int(os.path.split(filename)[1][:-4].split('.')[-2])

def matrixGPS(filename):
    """
    Returns GPS matrix read from a file
    """
    GPS = []
    with open(filename, 'r') as file:
        for l in file:
            values = l.strip().split()
            try:
                v = [float(i) for i in values]
            except ValueError:
                continue
            assert(len(v) == dim(filename)), 'Wrong dimension in' + filename
            GPS.append(v)
    return np.array(GPS)

def shapeDNA(filename):
    """
    Returns ShapeDNA vector read from a file
    """
    dna = []
    with open(filename, 'r') as file:
        for l in file:
            dna.append(float(l.strip()))
    assert(len(dna) == dim(filename)), 'Wrong dimension in' + filename
    return np.array(dna)
    
def regions(GPS):
    """
    Returns region indexes (0 to m - 1) for each vertex in GPS
    """
    global m
    distances = [np.linalg.norm(v) for v in GPS]
    d_min = min(distances)
    delta = (max(distances) - d_min) / m
    
    regs = [int((d - d_min) // delta) for d in distances]
    return regs

def samples(regions, m1, m2):
    """
    Computes 2 randomly sampled point indexes from regions m1 and m2, size prop% 
    """
    global m
    global prop
    assert(m1 < m and m2 < m), 'Regions given are not valid'
    np.random.seed(seed_)
    points_m1 = (np.array(regions) == m1).nonzero()[0]
    points_m2 = (np.array(regions) == m2).nonzero()[0]
    

    sample_m1 = np.random.choice(points_m1, int(prop * len(points_m1)))
    sample_m2 = np.random.choice(points_m2, int(prop * len(points_m2)))
    return sample_m1, sample_m2

def sample(regions, m1):
    """
    Computes randomly sampled point indexes from region m1, size prop% 
    """
    global m
    global prop
    assert(m1 < m), 'Region given are not valid'
    np.random.seed(seed_)
    points_m1 = (np.array(regions) == m1).nonzero()[0]
    sample_m1 = np.random.choice(points_m1, int(prop * len(points_m1)))
    
    return sample_m1

# def distances(GPS1, GPS2, regions1, regions2, m1, m2, metric='euclidean'):
    # """
    # Computes pair-wise distances between sampled points of GPS1 and GPS2 for regions m1 and m2 respectively
    # """
    # m1_indices = sample(regions1, m1)
    # m2_indices = sample(regions2, m2)
    # GPS_m1 = GPS1[m1_indices]
    # GPS_m2 = GPS2[m2_indices]
    # return cdist(GPS_m1, GPS_m2, metric=metric).flatten()

def distances(GPS, regions, m1, m2, metric='euclidean'):
    """
    Computes pair-wise distances between sampled points of GPS for regions m1 and m2
    """
    m1_indices, m2_indices = samples(regions, m1, m2)
    GPS_m1 = GPS[m1_indices]
    GPS_m2 = GPS[m2_indices]
    return cdist(GPS_m1, GPS_m2, metric=metric).flatten()

def myargwhere(l, value):
    """
    Returns indexes {i} in l where l[i] == value
    """
    return (np.array(l) == value).nonzero()[0]

def dim_reduction(X, method='tsne'):
    """
    Wrapper for different dimensionality reduction methods to plot found descriptors
    """
    if method == 'tsne':
        model = TSNE(n_components=2, perplexity=40, n_iter=300, random_state=seed_)
        coords_2d = model.fit_transform(X)
        return coords_2d[:, 0], coords_2d[:, 1]
    elif method == 'pca':
        model = PCA(n_components=2)
        coords_2d = model.fit_transform(X)
        return coords_2d[:, 0], coords_2d[:, 1]
    elif method == 'mds':
        model = MDS(n_components=2, max_iter=300, random_state=seed_)
        coords_2d = model.fit_transform(X)
        return coords_2d[:, 0], coords_2d[:, 1]
    else:
        raise Exception('Method is not valid')
        
def scatter_annotated(x, y, labels):
    """
    Plots a labeled scatter plot in matplotlib
    """
    fig, ax = plt.subplots(figsize=(10,10))
    for g in range(len(np.unique(labels))):
        label_i = np.unique(labels)[g]
        i = myargwhere(labels, label_i)
        ax.scatter(x[i], y[i], label=label_i)
    ax.legend()
    plt.show()

def G2_dist(embed1, embed2):
    d = 0
    for i in range(m):
        for j in range(i + 1):
            d += ks_2samp(list(embed1[i][j]), list(embed2[i][j]))[0]
    return d

assert(prop <= 1.0 and prop > 0.0), 'Proportion is not valid'
embeds = glob.glob(embeds_path + '/*.txt')
shapes = glob.glob(shapes_path + './**/*.obj')

# Split filename lists by descriptor
embeds_gps = []
embeds_shapedna = []
for i in embeds:
    if 'shapeDNA' in i:
        embeds_shapedna.append(i)
    else:
        embeds_gps.append(i)

miss = missing(embeds, shapes)
print('{} embeddings missing :\n'.format(len(miss)))
print(*miss, sep='\n')

# X stores ShapeDNA vectors, y stores complete labels (elephant-gallop-01, camel-collapse-20, etc.) and y_simple general labels (cat, face, etc.)
X = []
y_full = []
y_mid = []
y_simple = []
min_d = 20


int_table = str.maketrans(dict.fromkeys('0123456789'))
for f in embeds_shapedna:
    v = shapeDNA(f)
    X.append(v)
    if len(v) < min_d:
        min_d = len(v)
    meshname = name(f)
    y_full.append(meshname)
    y_simple.append(meshname.split('-')[0])
    y_mid.append(meshname.translate(int_table).strip('-').replace('-reference', '').split('--', 1)[0])

# truncate to maximum common spectrum depth
X_trunc = [x[:min_d] for x in X]
X_trunc = np.array(X_trunc)

print(X_trunc.shape)

# display shapeDNA embeddings
x_tsne, y_tsne = dim_reduction(X_trunc, method='tsne')
scatter_annotated(x_tsne, y_tsne, y_mid)

x_pca, y_pca = dim_reduction(X_trunc, method='pca')
scatter_annotated(x_pca, y_pca, y_mid)

x_mds, y_mds = dim_reduction(X_trunc, method='mds')
scatter_annotated(x_mds, y_mds, y_mid)


##### GPS Embeddings #####

# Histograms per shape (m = 1)
m = 1
base_names = list(set([meshname.split('-')[0] for meshname in embeds_gps]))

distribs = [[[None for _ in range(m)] for _ in range(m)] for _ in range(len(embeds_gps))]

for shape in base_names:
    # plt.figure(figsize=(15, 10))
    for shape_idx, f in enumerate(embeds_gps):
        if shape not in f:
            continue
        gps_i = matrixGPS(f)
        regs_i = regions(gps_i)
        for i in range(m):
            for j in range(i + 1):
                distribs[shape_idx][i][j] = distances(gps_i, regs_i, i, j)
        # sns.distplot(di, hist=False, label=f)
    # plt.title('G2 distributions for ' + shape +' shapes')
    # plt.show()

with open("./pickles/distribs.pickle", 'w') as pklF:
    pickle.dump(distribs, pklF)

# compute distance matrix
# dists = [[None] * len(embeds_gps) for _ in range(len(embeds_gps))]
# for i in range(len(embeds_gps)):
#     print("{}/{}".format(i, len(embeds_gps)))
#     for j in range(i + 1):
#         dists[i][j] = G2_dist(distribs[i], distribs[j])
#         dists[j][i] = dists[i][j]

# with open("./dists_matrix.pickle", 'w') as distF:
#     pickle.dump(dists, distF)

# embedder = MDS(dissimilarity='precomputed')
# embedding = embedder.fit_transform(dists)
