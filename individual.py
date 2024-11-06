import random
import numpy as np


class Individual:

    def __init__(self, n, empty=False):

        if empty:
            self.ind = np.empty(n, dtype=int)
        else:
            self.ind = np.arange(n)
            np.random.shuffle(self.ind)  # shuffles in place

        self.fitness = None
        self.F = None
        self.F2 = None
        
    def copy(self):
        x = Individual(self.n, empty=True)
        x.ind[:] = self.ind
        x.fitness = self.fitness
        x.F = self.F
        x.F2 = self.F2
        return x
            
    def evaluate(self, f):
        self.fitness, self.F, self.F2 = f(self.ind)
        
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
    
def cyclic_crossover(p1, p2):
    n = p1.n
    

    def create_child(p1, p2):
        ch = Individual(n, empty=True)
        ch.ind = np.full(n, -1, dtype=int)

        value1, value2 = p1.ind[0], p2.ind[0]
        i = 0 
        while True:
            ch.ind[i] = value1
        
            i = list(p1.ind).index(int(value2))
            value1, value2 = value2, p2.ind[i]
            if value1 in ch.ind:
                break
        for i, x in enumerate(ch.ind):
            if x == -1:
                ch.ind[i] = p2.ind[i]

        return ch

    ch1 = create_child(p1, p2)
    ch2 = create_child(p2, p1)
                
    return ch1, ch2

def partially_mapped_crossover(p1, p2):
    n = p1.n 
    c1 = np.random.randint(0, n)
    c2 = np.random.randint(c1+1, n+1)
    
    # print("p1:", p1)
    # print("p2:", p2)
    
    ch1 = Individual(n, empty=True)
    ch2 = Individual(n, empty=True)
    
    ch1.ind[c1:c2] = p2.ind[c1:c2]
    ch2.ind[c1:c2] = p1.ind[c1:c2]

    # print("ch1", ch1)
    # print("ch2", ch2)
    
    mapping1 = {
        p2.ind[i] : p1.ind[i]
        for i in range(c1, c2)
    }
    mapping2 = {
        p1.ind[i] : p2.ind[i]
        for i in range(c1, c2)
    }

    for i, x in enumerate(p1.ind):
        if c1 <= i < c2:
            continue
        first = True 
        k = 0 
        while x in ch1.ind[c1:c2]:
            if k == 100:
#                print("GAVE UP")
                return p1.copy(), p2.copy()
            k += 1
            #print(x, ch1.ind[c1:c2])
            if first:
                x = mapping1[x]
            else:
                x = mapping2[x]
            first = not first 
        ch1.ind[i] = x
     
    for i, x in enumerate(p2.ind):
        if c1 <= i < c2:
            continue
        first = True
        k = 1
        while x in ch2.ind[c1:c2]:
            if k == 100:
 #               print("GAVE UP")
                return p1.copy(), p2.copy()
            k += 1

            #print(x, ch2.ind[c1:c2])  
            if first:
                x = mapping2[x]
            else:
                x = mapping1[x]
            first = not first 
        ch2.ind[i] = x
     
#     assert len(ch1.ind) == n
#     assert len(ch2.ind) == n
            
#     for i in range(n):
# #        print(i)
#         assert i in ch1.ind, f"{i} {ch1}" 
#         assert i in ch2.ind, f"{i} {ch2}"

  #  print("PASSED")
    return ch1, ch2

def tournament_select(population):
    inds = np.random.choice(population, size=3, replace=False)
    best = None
    best_f = -100000000000
    best_c = 100000 # TODO put here someting reasonable
    best_c2 = -100000000000
    for ind in inds:
        if ind.fitness > best_f:
            best = ind
            best_f = ind.fitness
            best_c = ind.F
            best_c2 = ind.F2
        elif ind.fitness ==  best_f and ind.F2 > best_c2:
            best = ind
            best_f = ind.fitness
            best_c = ind.F
            best_c2 = ind.F
        elif ind.fitness ==  best_f and ind.F2 == best_c2 and ind.F < best_c:
            best = ind
            best_f = ind.fitness
            best_c = ind.F
            best_c2 = ind.F            
    assert best is not None
    return best

def roulette_select(population):
    f = np.array([-i.fitness for i in population])
    f = 1/(f+0.0000001)
    f = f / f.sum()
    return np.random.choice(population,  p=f)



def mutate(ind):

    pos1, pos2 = np.random.choice(ind.n, size=2, replace=False)
    ind.ind[pos1], ind.ind[pos2] = ind.ind[pos2], ind.ind[pos1]
    
class Mutation():
    def __init__(self, vertices, centralities, centralities2):
        self.vertices = vertices
        self.centralities = centralities
        self.centralities2 = centralities2
        
    def mutate(self, ind):
        n = ind.n
        m = random.randrange(1,5)
        for _ in range(1):
            #    criterion = self.vertices  #+ self.centralities2
            criterion = self.centralities2
            
            pos = random.randrange(n)
            """
            xxx = np.abs(criterion - criterion[ind.ind])
            if xxx.sum() == 0:
                pos = random.randrange(n)
            else:
                xxx = xxx / xxx.sum()
                pos = np.random.choice(n, size=1, p=xxx)
            """
            """
            r = np.random.random()
            if r  < 0.3:
            criterion = self.vertices
            elif r < 0.6:
            criterion = self.centralities
            else:
            criterion = self.centralities2
            """
            #criterion = self.centralities + self.centralities2 + self.vertices
            cost = np.abs(criterion - criterion[ind.ind[pos]]) #/(criterion+criterion[ind.ind[pos]])
            + np.abs(criterion[ind.ind] - criterion[pos]) #/(criterion[ind.ind]+criterion[pos])
            #- np.abs(criterion - criterion[ind.ind]) #/(criterion+criterion[ind.ind])
            possibilities = 1/(cost + 0.000001)
            possibilities[pos] = 0
            possibilities[ind.ind[pos]] = 0
            #        possibilities[ind.ind[pos]] = np.quantile(possibilities[possibilities != 0], 0.1)
            possibilities /= possibilities.sum()
            if len(possibilities) > 0:
                pos2 = np.random.choice(n, p=possibilities)
                ind.ind[pos], ind.ind[pos2] = ind.ind[pos2], ind.ind[pos]
            
