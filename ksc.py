'''
This implementation is invariant to time. 
That is, it does not account for different values
of q in the original paper: 
http://snap.stanford.edu/data/ksc.html

Inputs: 
- vocab.text: list of vocab, in the same order as time_series.npy
- time_series.npy: a matrix where each row is a time series of a word 

Outputs: 
- mu_k.npy: centroids of each cluster
- clusters_set_k.npy: the cluster assignments of each time series 
'''


import random
import numpy as np 
from collections import defaultdict
from numpy import linalg as LA
from copy import deepcopy

def cluster_time_series(k): 
    
    random.seed(0)
    word_list = []
    with open('vocab.txt', 'r') as infile: 
            for line in infile: 
                word_list.append(line.strip())
    matrix = np.load('time_series.npy')
    # N = number of time series
    N = matrix.shape[0]
    
    # cluster membership for each time series
    mem = np.array([random.randint(0, k-1) for idx in range(N)])
    
    # optimal alpha, as defined in the paper
    alpha = lambda x, y: np.dot(x, y) / np.dot(y, y)
    
    # d^ as defined in the paper
    d_hat = lambda x, y: (np.linalg.norm(x - alpha(x,y)*y)) / (np.linalg.norm(x))
    
    for it in range(100):
        print("Iteration", it)
        prev_mem = deepcopy(mem)
        mu = np.zeros((k, matrix[0].shape[0]))
        for j in range(k):
            A = []
            for vec_idx in range(N): 
                if mem[vec_idx] == j: 
                    vec = matrix[vec_idx]
                    A.append(vec)
            A = np.array(A)
            if A.shape[0] == 0: 
                mu[j] = np.zeros(matrix[0].shape[0])
                continue
            interm = np.sqrt(np.sum(np.square(A), 1))
            B = np.divide(A, np.tile(interm, (A.shape[1], 1)).transpose())
            M = np.matmul(np.transpose(B), B) - A.shape[0]*np.identity(A.shape[1])
            w, v = LA.eig(M)
            idx = np.argmin(np.absolute(w))
            if np.sum(v[:,idx]) < 0: 
                mu[j] = -v[:,idx]
            else: 
                mu[j] = v[:,idx]

        for vec_idx in range(N): 
            vec = matrix[vec_idx]
            distances = []
            for j in range(k): 
                distances.append(d_hat(vec, mu[j]))
            j_star = np.argmin(distances)
            mem[vec_idx] = j_star
            
        if np.linalg.norm(prev_mem - mem) == 0: 
            break
    np.save('mu_' + str(k) + '.npy', mu)
    np.save('clusters_set_' + str(k) + '.npy', mem)
    
def main(): 
    # k = 6
    cluster_time_series(6)

if __name__ == '__main__':
    main()
