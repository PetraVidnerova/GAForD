
import multiprocessing
import random

import numpy as np

from individual import Individual, order_crossover, tournament_select, mutate, cyclic_crossover, partially_mapped_crossover, Mutation
from fitness import Fitness
from population import Population


class F():

    def evaluate(self, individual):
        return (individual == np.arange(10)).sum(), 0


#f = F()

f = Fitness("data/LRM_ER_rewired/LRM_ER_nNodes50_rew0_sim0.csv")
print(f.matrix)

vertices = f.matrix.sum(axis=1)
mutation = Mutation(vertices)

N = 120  # size of populations
n = 50
k = 20   # number of populations

PCX = 0.9
PMUT = 0.2
steps = 100


def run(pop):
    return pop.run(PCX, PMUT, steps=steps), pop


def islands():
    populations = []
    for i in range(k):
        pop = Population(n, N, f, mutation)
        populations.append(pop)

    fitnesses = [ind.fitness for ind in pop.population]
    print(max(fitnesses), np.mean(fitnesses))

    pool = multiprocessing.Pool(10)
    gen = 0
    while True:

        #        with multiprocessing.Pool(10) as pool:
        ret = pool.map(run, populations)
        ret = list(ret)
        populations = [x[1] for x in ret]
        results = [x[0] for x in ret]
        print(gen, ":", results)
        gen += steps

        if gen % 1000 == 0:
            elittes = [pop.elitte for pop in populations]
            # print(elittes)
            for pop, elitte in zip(populations, elittes[1:]+elittes[:1]):
                # pop.update_elitte(elitte[0])
                pop.update_elitte(elitte[0])
            # for i, e in enumerate(elittes):
            #    for j, pop in enumerate(populations):
            #        if i != j:
            #            pop.update_elitte([e[0]])

#            for pop, elitte in zip(populations, elittes[-1:]+elittes[:-1]):
#                pop.update_elitte(elitte)

            #pop = random.choice(populations)
            if gen % 20000 == 0:
                for pop in populations:
                    pop.restart()

#            print(elittes)
            l = [ i for e in elittes for i in e]
 #           print(l)
            inds = sorted(l, key=lambda x: x.fitness, reverse=True)
            print(inds[0].fitness, inds[0].F)
            print(inds[0].ind)
            if inds[0].fitness == 0:
                return
    

def single():

    pop = Population(n, N, f)
    gen = 0
    while True:

        ret = run(pop)
        
        print(gen, ":", ret)
        gen += 100

        if gen % 1000 == 0: 
            inds = sorted([ i for i in pop.elitte], key=lambda x: x.fitness, reverse=True)
            print(inds[0].fitness, inds[0].F)
            print(inds[0].ind)
    
if __name__ == "__main__":

    islands()
    #single()
