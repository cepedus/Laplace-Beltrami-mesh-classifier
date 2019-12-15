import glob
import numpy as np
import pickle
from scipy.spatial.distance import cdist
import os


seed_ = 42
embeds_path = './results'
prop = 0.05


def dim(filename):
    """
    Given an embedding filename, returns how many eigs were supposedly computed
    """
    return int(os.path.split(filename)[1][:-4].split('.')[-2])


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

def distances(GPS, regions, m1, m2, metric='euclidean'):
    """
    Computes pair-wise distances between sampled points of GPS for regions m1 and m2
    """
    m1_indices, m2_indices = samples(regions, m1, m2)
    GPS_m1 = GPS[m1_indices]
    GPS_m2 = GPS[m2_indices]
    return cdist(GPS_m1, GPS_m2, metric=metric).flatten()



embeds = glob.glob(embeds_path + '/*.txt')

# Split filename lists by descriptor
embeds_gps = []
embeds_shapedna = []
for i in embeds:
    if 'shapeDNA' in i:
        embeds_shapedna.append(i)
    else:
        embeds_gps.append(i)

# Histograms per shape (m = 1)
m = 1
base_names = list(set([meshname.split('-')[0] for meshname in embeds_gps]))

distribs = [[[None for _ in range(m)] for _ in range(m)] for _ in range(len(embeds_gps))]

for shape in base_names:
    for shape_idx, f in enumerate(embeds_gps):
        if shape not in f:
            continue
        gps_i = matrixGPS(f)
        regs_i = regions(gps_i)
        for i in range(m):
            for j in range(i + 1):
                distribs[shape_idx][i][j] = distances(gps_i, regs_i, i, j)


with open("../../pickles/distribs.pickle", 'wb') as pklF:
    pickle.dump(distribs, pklF)