
import numpy as np

def calculate_centralities(A):
    #https://stackoverflow.com/questions/75290487/bonacich-centrality-in-python
    centrality = np.dot(A,A)
    row_sum = np.sum(centrality, axis=1)
    total_of_row = sum(row_sum)
    row_sum_normalized = row_sum * 1/total_of_row
    return row_sum_normalized


class Fitness:
    def __init__(self, filename):
        self.matrix = np.loadtxt(filename, delimiter=",").astype(int)

        self.vertices = self.matrix.sum(axis=1)

        self.centralities = calculate_centralities(self.matrix)
        
    def evaluate(self, individual):
        permutation = individual

        n, _ = self.matrix.shape

        if np.all(permutation == range(n)):
            return -100, 100, -100

        matrix2 = np.zeros(self.matrix.shape)

        fix_points =  (permutation == range(n)).sum()

        #same_vertices = (self.vertices[permutation] == self.vertices).sum()
        same_vertices = (
            np.abs(self.centralities[permutation] - self.centralities).sum() +
            np.abs(self.vertices[permutation] - self.vertices).sum()
        )
        
        for i, j in zip(*self.matrix.nonzero()):
            x, y = permutation[i], permutation[j]
#            if (x, y) == (i, j):
#                fix_points += 1
            matrix2[x, y] = 1

        return (
#            - (np.absolute((self.matrix - matrix2)).sum())/ (n*(n-1)/2 - fix_points*(fix_points-1)/2),
            - 10*same_vertices - (np.absolute((self.matrix - matrix2)).sum())/ (n*(n-1)/2)
            - (fix_points/n),
#            - same_vertices - 0.001*fix_points/n - (np.absolute((self.matrix - matrix2)).sum())/ (n*(n-1)/2),
            fix_points,
            - (np.absolute((self.matrix - matrix2)).sum())/ (n*(n-1)/2)
            )
