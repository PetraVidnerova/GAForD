import pickle
import networkx as nx
import numpy as np

def calculate_centralities(A):
    #https://stackoverflow.com/questions/75290487/bonacich-centrality-in-python
    centrality = np.dot(A,A)
    row_sum = np.sum(centrality, axis=1)
    total_of_row = sum(row_sum)
    row_sum_normalized = row_sum * 1/total_of_row
    return row_sum_normalized

def calculate_centralities2(A):
    g = nx.from_numpy_array(A)
    #return np.array([x for x in nx.eigenvector_centrality(g).values()])
    return np.array([x for x in nx.betweenness_centrality(g).values()])

def calculate_degree_centrality(A):
    g = nx.from_numpy_array(A)
    return np.array([x for x in nx.degree_centrality(g).values()])
    # return np.array([x for x in nx.pagerank(g).values()])

class Fitness:
    def __init__(self, filename, sim):
        
        with open(filename, "rb") as f:
            source = pickle.load(f)

        self.matrix = source[sim]
        
        #        self.matrix = np.loadtxt(filename, delimiter=",").astype(int)

        #self.vertices = self.matrix.sum(axis=1)
        self.vertices = calculate_degree_centrality(self.matrix)
        
        self.centralities = calculate_centralities(self.matrix)

        self.centralities2 = calculate_centralities2(self.matrix) 
        
        
    def evaluate(self, individual):
        permutation = individual

        n, _ = self.matrix.shape

        if (permutation == range(n)).sum() > 0: #> n/10:
            return -1000000, 1000000, -1000000

        matrix2 = np.zeros(self.matrix.shape)
        matrix3 = np.zeros(self.matrix.shape)

        fix_points =  (permutation == range(n)).sum()

        bitmap = permutation != range(n)
        #sam_vertices = (self.vertices[permutation] == self.vertices).sum()
        same_vertices = n*(
            np.abs(self.centralities[permutation[bitmap]] - self.centralities[bitmap]).sum() +
            np.abs(self.centralities2[permutation[bitmap]] - self.centralities2[bitmap]).sum() +
            np.abs(self.vertices[permutation[bitmap]] - self.vertices[bitmap]).sum()
        )/(3*bitmap.sum())
        
        for i, j in zip(*self.matrix.nonzero()):
            x, y = permutation[i], permutation[j]
            if x != i or y !=j:
                matrix3[x, y] = 1
#            if (x, y) == (i, j):
#                fix_points += 1
            matrix2[x, y] = 1

        return (
#            - (np.absolute((self.matrix - matrix2)).sum())/ (n*(n-1)/2 - fix_points*(fix_points-1)/2),
            -(np.absolute((self.matrix - matrix2)).sum())/ n*(n-1)/2 #- fix_points*(fix_points-1)/2)
            - 10*same_vertices,
            #            - 0.1*(np.absolute((self.matrix - matrix2)).sum())/(n*(n-1)/2),
#            - (fix_points/n),
#            - same_vertices - 0.001*fix_points/n - (np.absolute((self.matrix - matrix2)).sum())/ (n*(n-1)/),
            fix_points,
            - (np.absolute((self.matrix - matrix2)).sum())#/2# (n*(n-1)/2)z
            )
