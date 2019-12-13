import sys
import pickle
from scipy.stats import ks_2samp


i = int(sys.argv[1])
n = int(sys.argv[2])
m = int(sys.argv[3])

def G2_dist(embed1, embed2):
    d = 0
    for i in range(m):
        for j in range(i + 1):
            d += ks_2samp(embed1[i][j], embed2[i][j])[0]
    return d



with open("./pickles/distribs.pickle", 'rb') as pklF:
    distribs = pickle.load(pklF)



# compute distance matrix
dists = [None] * n
for j in range(i + 1):
    dists[j] = G2_dist(distribs[i], distribs[j])

with open("./pickles/dists_{}.pickle".format(i), 'wb') as distF:
    pickle.dump(dists, distF)
