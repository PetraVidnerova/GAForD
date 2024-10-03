import numpy as np

class Fitness:
    def __init__(self, filename):
        self.matrix = np.loadtxt(filename, delimiter=",").astype(int)
        
    def evaluate(self, individual):
        permutation = individual

        n, _ = self.matrix.shape

        if np.all(permutation == range(n)):
            return -100

        matrix2 = np.zeros(self.matrix.shape)

        fix_points =  (permutation == range(n)).sum()
        for i, j in zip(*self.matrix.nonzero()):
            x, y = permutation[i], permutation[j]
#            if (x, y) == (i, j):
#                fix_points += 1
            matrix2[x, y] = 1

        return (
            - (np.absolute((self.matrix - matrix2)).sum())/ (n*(n-1)/2 - fix_points*(fix_points-1)/2),
            fix_points
        )
            
