import multiprocessing
import random

import click
import numpy as np


from individual import Individual, order_crossover, tournament_select, mutate, cyclic_crossover, partially_mapped_crossover, Mutation
from fitness import Fitness
from population import Population


class F():

    def evaluate(self, individual):
        return (individual == np.arange(10)).sum(), 0


#f = F()


#vertices = f.matrix.sum(axis=1)
#mutation = Mutation(vertices)

N = 60 #120 # size of populations
n = 50
k = 10 #30   # number of populations

PCX = 0.95 # 0.95
PMUT = 0.15
steps = 100


def run(pop):
    return pop.run(PCX, PMUT, steps=steps), pop

@click.command()
@click.argument('sourcename')
def islands(sourcename):
    
    f = Fitness(sourcename)
    print(f.matrix)


    populations = []
    for i in range(k):
        pop = Population(n, N, f, None)
        populations.append(pop)

    fitnesses = [ind.fitness for ind in pop.population]
    print(max(fitnesses), np.mean(fitnesses))

    pool = multiprocessing.Pool(25)
    gen = 0
    last_best = None
    stay_same = 0
    while True:

        #        with multiprocessing.Pool(10) as pool:
        ret = pool.map(run, populations)
        ret = list(ret)
        populations = [x[1] for x in ret]
        results = [x[0] for x in ret]
        print(gen, ":", results, flush=True)
        gen += steps

        if True: #gen % 100 == 0:
            elittes = [pop.elitte for pop in populations]
            # print(elittes)
#            for pop, elitte in zip(populations, elittes[1:]+elittes[:1]):
#                pop.update_elitte(elitte)

            #               pop.update_elitte(elitte[0])
            for i, e in enumerate(elittes):
                for j, pop in enumerate(populations):
                    if i != j:
                        pop.update_elitte(e)


            #pop = random.choice(populations)
            #if gen % 20000 == 0:
            #    for pop in populations:
            #        pop.restart()

#            print(elittes)
            l = [ i for e in elittes for i in e]
 #           print(l)
            inds = sorted(l, key=lambda x: x.fitness, reverse=True)
            print("RESULT:", inds[0].fitness, inds[0].F, inds[0].F2)
            print(inds[0].ind)
            best = (inds[0].fitness, inds[0].F, inds[0].F2)
            if inds[0].F2 == 0:
                print("Solution found.")
                return
            
            if best == last_best:
                stay_same += 1
                if stay_same == 50:
                    print(" No progress. Exiting. ")
                    return # END OF THE WHOLE THING
                if stay_same % 10 == 0:
                    # restarting
                    print(" * *** * RESTARTING * ** * ")
                    for pop in populations:
                        pop.restart()
                    all_elitte = []
                    for pop in populations:
                        elittes = pop.elitte
                        pop.elitte = []
                        for elitte in elittes:
                            same = False
                            for e in all_elitte:
                                if np.all(e.ind == elitte.ind):
                                    same = True
                                    break
                            if not same:
                                all_elitte.append(elitte)
                    print("LEN", len(all_elitte))
                    for i, pop in enumerate(populations):
                        if i < len(all_elitte):
                            pop.elitte = [all_elitte[i]]
                        else:
                            pop.elitte = []

#                    for pop in populations:
#                        print(pop.elitte[0].fitness, pop.elitte[0].F, pop.elitte[0].ind)
                            
                else:
                    print(" * *** * MIXING POPULATIONS * ** *")
                    # mix populations somehow
                    kk = N // 3
                    groups = []
                    for pop in populations: 
                        group = pop.extract(kk)
                        groups.append(group)
                    for i, pop in enumerate(populations):
                        pop.append(groups[ (i+1) % k])
            else:
                last_best = best    
                stay_same = 0
            
#        if gen >= 10000:
#            return
        
@click.command()
@click.argument('sourcename')
def single(sourcename):

    f = Fitness(sourcename)
    print(f.matrix)

    
    pop = Population(n, N, f, None)
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
#    single()
