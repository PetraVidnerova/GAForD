import numpy as np

class Individual:

    def __init__(self, n, empty=False):

        if empty:
            self.ind = np.empty(n, dtype=int)
        else:
            self.ind = np.arange(n)
            np.random.shuffle(self.ind) # shuffles in place

        self.fitness = None
            
    def eval(self, f):
        self.fitness = f(self.ind)
        
    @property
    def n(self):
        return len(self.ind)
        

    def __str__(self):
        return "-".join([f"{x}" for x in self.ind])

def fitness(ind):
    target = np.arange(ind.n)
    return np.mean(target == ind.ind)

    
def order_crossover(p1, p2):

    n = p1.n
    assert p1.n == p2.n

    c1 = np.random.randint(0, n)
    c2 = np.random.randint(c1+1, n+1)

    # print(p1.ind[:c1], " --- ", p1.ind[c1:c2], " --- ", p1.ind[c2:])
    # print(p2.ind[:c1], " --- ", p2.ind[c1:c2], " --- ", p2.ind[c2:])
    
    ch1 = Individual(n, empty=True)
    ch2 = Individual(n, empty=True)

    ch1.ind[c1:c2] = p2.ind[c1:c2]
    ch2.ind[c1:c2] = p1.ind[c1:c2]


    def copy_in_order(child, parent):
        j = 0
        for i in range(n):
            if  c1 <= i < c2:
                continue
            while parent.ind[j] in child.ind[c1:c2]:
                j += 1
            child.ind[i] = parent.ind[j]
            j += 1
    
    copy_in_order(ch1, p1)
    copy_in_order(ch2, p2)

    
    return ch1, ch2
    
