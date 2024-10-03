import random
import numpy as np
from individual import Individual, order_crossover, tournament_select, mutate, cyclic_crossover, partially_mapped_crossover


class Population():

    def __init__(self, n, N, fitness, mutation):

        self.n = n
        self.N = N
        self.fitness = fitness
        self.mutation = mutation

        self.population = []
        for i in range(N):
            self.population.append(Individual(n))

        for ind in self.population:
            ind.evaluate(fitness.evaluate)

        self.elitte_size = 3
        self.elitte = []

    def restart(self):
        #self.population = []
        for i in range(self.N):
            if i % 2 == 0:
                self.population[i] = Individual(self.n)
                self.population[i].evaluate(self.fitness.evaluate)

    def update_elitte(self, elitte):

     #       print([x.fitness for x in self.elitte])
     #       print([x.fitness for x in elitte])
        # $#        self.population.extend(elitte)
        #        self.elitte = sorted(self.elitte + elitte, key=lambda x: x.fitness, reverse=True)[:self.elitte_size]
        #        self.elitte = elitte
        # for e in self.elitte:
        #    if np.all(e.ind == elitte.ind):
        #        return
        # self.population.append(elitte)

        #        print([x.fitness for x in self.elitte])
        #        exit()
        for e in self.elitte:
            if np.all(e.ind == elitte.ind):
                return
        self.elitte.append(elitte)
#        self.elitte = elitte
        
    def run(self, pcx, pmut, steps=1):
        for _ in range(steps):
            ret = self.step(pcx, pmut)
        return ret
            
    def step(self, pcx, pmut):
        new_pop = []
        new_pop.extend(self.elitte)
    
        while len(new_pop) < self.N:
            p1 = tournament_select(self.population)
            p2 = tournament_select(self.population)

            # cx = np.random.choice([order_crossover, cyclic_crossover, partially_mapped_crossover],
            #                       p=[0.45, 0.54, 0.01])
            #cx = cyclic_crossover
            cx = np.random.choice([order_crossover, cyclic_crossover], p=(0.5, 0.5))
            if np.random.random() < pcx:
                ch1, ch2 = cx(p1, p2)
                ch1.evaluate(self.fitness.evaluate)
                ch2.evaluate(self.fitness.evaluate)
            else:
                ch1, ch2 = p1.copy(), p2.copy()

            for child in ch1, ch2:
                if np.random.random() < pmut:
                    mutate(child) #mutation in place
                    child.evaluate(self.fitness.evaluate)
                    
            new_pop.append(ch1)
            new_pop.append(ch2)
        
        self.population = sorted(new_pop, key=lambda x: x.fitness, reverse=True)
        #self.elitte = self.population[:self.elitte_size]
        self.elitte = []
        for i in self.population:
            for e in self.elitte:
                if np.all(e.ind == i.ind):
                    continue
            self.elitte.append(i.copy())
            if len(self.elitte) >= self.elitte_size:
                break
        
        return float(-self.population[0].fitness), float(-np.mean([i.fitness for i in self.population]))

